from django.contrib.auth.models import User
from django.test import TestCase


class AccountTests(TestCase):
    def test_register_creates_user_and_redirects(self):
        response = self.client.post('/register/', {
            'username': 'arshi', 'email': 'arshi@example.com',
            'password': 'StrongPassword123!',
        })
        self.assertRedirects(response, '/login/')
        self.assertTrue(User.objects.filter(username='arshi').exists())

    def test_duplicate_username_is_rejected(self):
        User.objects.create_user(username='arshi', password='StrongPassword123!')
        response = self.client.post('/register/', {
            'username': 'arshi', 'email': 'another@example.com',
            'password': 'StrongPassword123!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.filter(username='arshi').count(), 1)

    def test_login_and_protected_dashboard(self):
        User.objects.create_user(username='arshi', password='StrongPassword123!')
        self.assertRedirects(self.client.get('/dashboard/'), '/login/?next=/dashboard/')
        response = self.client.post('/login/', {
            'username': 'arshi', 'password': 'StrongPassword123!',
        })
        self.assertRedirects(response, '/dashboard/')
        self.assertEqual(self.client.get('/dashboard/').status_code, 200)
