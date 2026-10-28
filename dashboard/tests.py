from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase

from alerts.models import Alert


class DashboardTests(TestCase):
    @patch('dashboard.views.get_live_price', return_value=Decimal('120.00'))
    def test_dashboard_only_shows_own_alerts(self, price):
        owner = User.objects.create_user('owner')
        other = User.objects.create_user('other')
        for user, ticker in [(owner, 'INFY'), (other, 'TCS')]:
            Alert.objects.create(
                user=user, ticker=ticker, company=ticker,
                yahoo_symbol=f'{ticker}.NS', asset_type='stock',
                condition='above', target_price=Decimal('100.00'),
            )
        self.client.force_login(owner)
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'INFY')
        self.assertNotContains(response, 'TCS')
        price.assert_called_once_with('INFY.NS')
