from django.test import TestCase, Client
from .models import User


class AuthenticationTest(TestCase):
    def setUp(self):
        # Create user
        User.objects.create_user(username='testuser', password='password', email='testuser@example.com')

    def test_registration_form(self):
        client = Client()

        # '200 OK' should be returned for a registration page GET request
        response = client.get('/register/')
        self.assertEqual(response.status_code, 200)

        # '302 FOUND' should be returned (redirection on success)
        response = client.post('/register/', {
            'username': 'postuser',
            'email': 'testuser@example.com',
            'password1': 'Tr0ub4dor&3',
            'password2': 'Tr0ub4dor&3',
            'remember_me': 'on'
        })
        self.assertEqual(response.status_code, 302)

        # '200 OK' should be returned as a user with these credentials is already registered
        response = client.post('/register/', {
            'username': 'postuser',
            'email': 'testuser@example.com',
            'password1': 'Tr0ub4dor&3',
            'password2': 'Tr0ub4dor&3',
            'remember_me': 'on'
        })
        self.assertEqual(response.status_code, 200)

    def test_login_form(self):
        client = Client()
        # client.login(username='testuser', password='password')

        # '200 OK' should be returned for a login page GET request
        response = client.get('/login/')
        self.assertEqual(response.status_code, 200)

        # '200 OK' should be returned due to the incorrect password
        response = client.get('/login/', {
            'username': 'testuser',
            'password': 'incorrect_password'
        })
        self.assertEqual(response.status_code, 200)

        # '302 FOUND' should be returned (redirection on success)
        response = client.post('/login/', {
            'username': 'testuser',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 302)

        # '200 OK' should be returned for logout GET request
        response = client.get('/logout/')
        self.assertEqual(response.status_code, 200)

        # False should be returned, because after logging out the user shouldn't be authenticated
        self.assertFalse(response.context['user'].is_authenticated)
