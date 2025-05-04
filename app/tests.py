from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse


class AuthTest(APITestCase):
    def setUp(self):
        self.regis_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')

        self.user_data = {
            'username': 'user',
            'password': 'user',
        }

        self.client.post(self.regis_url, self.user_data)
        response = self.client.post(self.login_url, self.user_data)
        # self.client.post(self.logout_url, self.user_data)
        self.refresh_token = response.data['refresh']
        self.access_token = response.data['access']


    def test_regis(self):
        data = {
            'username': 'user1',
            'password': 'user1'
        }

        response = self.client.post(self.regis_url, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['data'], 'user1')
        self.assertEqual(response.data['msg'], "Siz ro'yxatdan o'tdingiz!")


    def test_login(self):
        response = self.client.post(self.login_url, self.user_data)

        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)
        self.assertEqual(response.status_code, 200)


    def test_logout(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        response = self.client.post(self.logout_url, {"refresh": self.refresh_token})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['msg'], 'Tizimdan chiqdingiz!')

    def test_logout_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        response = self.client.post(self.logout_url, {"refresh": "invalid_refresh_token"})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['msg'], "Token noto'g'ri!")