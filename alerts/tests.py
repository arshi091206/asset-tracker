from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.management import call_command
from django.core import mail
from django.test import SimpleTestCase, TestCase
from django.test.utils import override_settings

from .asset_loader import get_asset, search_assets
from .models import Alert
from .notifications import send_alert_email
from .services import check_all_alerts
from .utils import get_live_price


class AssetLoaderTests(SimpleTestCase):
    def test_lookup_and_search(self):
        asset = get_asset('Infosys Limited')
        self.assertEqual(asset['yahoo_symbol'], 'INFY.NS')
        self.assertIn(asset, search_assets('info'))
        self.assertIsNone(get_asset('Not a real company'))


class PriceTests(SimpleTestCase):
    @patch('alerts.utils.yf.Ticker')
    def test_live_price(self, ticker):
        history = ticker.return_value.history.return_value
        history.empty = False
        history.__getitem__.return_value.iloc.__getitem__.return_value = 123.45
        self.assertEqual(get_live_price('INFY.NS'), 123.45)
        ticker.assert_called_once_with('INFY.NS')

    @patch('alerts.utils.yf.Ticker')
    def test_missing_price(self, ticker):
        ticker.return_value.history.return_value.empty = True
        self.assertIsNone(get_live_price('INFY.NS'))


class AlertViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('owner', password='StrongPassword123!')
        self.other = User.objects.create_user('other', password='StrongPassword123!')
        self.client.force_login(self.user)

    def make_alert(self, user=None):
        return Alert.objects.create(
            user=user or self.user, ticker='INFY', company='Infosys Limited',
            yahoo_symbol='INFY.NS', asset_type='stock', condition='above',
            target_price=Decimal('100.00'),
        )

    def test_create_alert_from_catalog(self):
        response = self.client.post('/alerts/create/', {
            'company': 'Infosys Limited', 'condition': 'above',
            'target_price': '100.00',
        })
        self.assertRedirects(response, '/dashboard/')
        alert = Alert.objects.get(user=self.user)
        self.assertEqual(alert.yahoo_symbol, 'INFY.NS')
        self.assertEqual(alert.target_price, Decimal('100.00'))

    def test_unknown_company_does_not_create_alert(self):
        response = self.client.post('/alerts/create/', {
            'company': 'Unknown', 'condition': 'above', 'target_price': '100.00',
        })
        self.assertRedirects(response, '/alerts/create/')
        self.assertFalse(Alert.objects.exists())

    def test_edit_alert(self):
        alert = self.make_alert()
        response = self.client.post(f'/alerts/edit/{alert.pk}/', {
            'company': 'Infosys Limited', 'condition': 'below',
            'target_price': '95.00',
        })
        self.assertRedirects(response, '/dashboard/')
        alert.refresh_from_db()
        self.assertEqual(alert.condition, 'below')
        self.assertEqual(alert.target_price, Decimal('95.00'))

    def test_other_user_cannot_read_edit_or_delete_alert(self):
        alert = self.make_alert(self.other)
        self.assertEqual(self.client.get(f'/alerts/{alert.pk}/').status_code, 404)
        self.assertEqual(self.client.get(f'/alerts/edit/{alert.pk}/').status_code, 404)
        self.assertEqual(self.client.get(f'/alerts/delete/{alert.pk}/').status_code, 404)
        self.assertTrue(Alert.objects.filter(pk=alert.pk).exists())

    def test_search_endpoint(self):
        response = self.client.get('/alerts/search/', {'q': 'info'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(any(row['name'] == 'Infosys Limited' for row in response.json()))


class AlertServiceTests(TestCase):
    def setUp(self):
        user = User.objects.create_user('owner', email='owner@example.com')
        self.alert = Alert.objects.create(
            user=user, ticker='INFY', company='Infosys Limited',
            yahoo_symbol='INFY.NS', asset_type='stock', condition='above',
            target_price=Decimal('100.00'),
        )

    @patch('alerts.services.send_alert_email')
    @patch('alerts.services.get_live_price', return_value=Decimal('120.00'))
    def test_sends_once_when_threshold_is_reached(self, price, send_email):
        check_all_alerts()
        check_all_alerts()
        self.alert.refresh_from_db()
        self.assertTrue(self.alert.triggered)
        self.assertTrue(self.alert.notification_sent)
        send_email.assert_called_once_with(self.alert)
        self.assertEqual(price.call_count, 2)

    @patch('alerts.services.send_alert_email')
    @patch('alerts.services.get_live_price', return_value=Decimal('90.00'))
    def test_no_email_below_threshold(self, price, send_email):
        check_all_alerts()
        self.alert.refresh_from_db()
        self.assertFalse(self.alert.triggered)
        self.assertFalse(self.alert.notification_sent)
        send_email.assert_not_called()

    @patch('alerts.services.send_alert_email')
    @patch('alerts.services.get_live_price', return_value=None)
    def test_unavailable_price_does_not_change_alert(self, price, send_email):
        check_all_alerts()
        self.alert.refresh_from_db()
        self.assertFalse(self.alert.triggered)
        self.assertFalse(self.alert.notification_sent)
        send_email.assert_not_called()

    @patch('alerts.services.send_alert_email')
    @patch('alerts.services.get_live_price', return_value=Decimal('90.00'))
    def test_below_condition_triggers(self, price, send_email):
        self.alert.condition = 'below'
        self.alert.save()
        check_all_alerts()
        self.alert.refresh_from_db()
        self.assertTrue(self.alert.triggered)
        send_email.assert_called_once()

    @patch('alerts.services.send_alert_email')
    @patch('alerts.services.get_live_price')
    def test_inactive_alert_is_skipped(self, price, send_email):
        self.alert.is_active = False
        self.alert.save()
        check_all_alerts()
        price.assert_not_called()
        send_email.assert_not_called()

    @override_settings(
        EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
        EMAIL_HOST_USER='test@example.com',
    )
    def test_notification_goes_to_alert_owner(self):
        send_alert_email(self.alert)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['owner@example.com'])
        self.assertIn('INFY', mail.outbox[0].subject)

    @patch('alerts.services.check_all_alerts')
    def test_management_command_calls_service(self, check):
        call_command('check_alerts')
        check.assert_called_once_with()
