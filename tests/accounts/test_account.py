from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import PoliceUser


class PoliceLoginTest(APITestCase):
    def setUp(self):
        self.email = 'juan@police.com'
        self.password = 'nuevaPass123PO'
        self.user = PoliceUser.objects.create_user(
            username=self.email,
            email=self.email,
            password=self.password,
        )
        self.user.set_password(self.password)
        self.user.save()
        self.login_url = reverse('token_obtain')

    def test_login_with_valid_credentials(self):
        response = self.client.post(self.login_url, {
            'email': self.email,
            'password': self.password
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_with_invalid_credentials(self):
        response = self.client.post(self.login_url, {
            'email': self.email,
            'password': 'contraseñaerronea'
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('access', response.data)

    def test_login_with_invalid_email(self):
        response = self.client.post(self.login_url, {
            'email': 'email@noregistrado.com',
            'password': self.password
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('access', response.data)

    def test_login_with_missing_fields(self):
        response = self.client.post(self.login_url, {
            'email': self.email,
            # missing password
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
