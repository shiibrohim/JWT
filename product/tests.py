from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


class ProductTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='pass')
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        self.product_data = {
            "name": "product",
            "desc": "desc",
            "price": "44.000"
        }

        self.create_url = reverse('create')
        self.list_url = reverse('list')
        response = self.client.post(self.create_url, self.product_data)
        self.product_id = response.data['id']
        self.detail_url = reverse('detail', kwargs={'pk': self.product_id})
        self.update_url = reverse('update', kwargs={'pk': self.product_id})
        self.delete_url = reverse('delete', kwargs={'pk': self.product_id})

    def test_create(self):
        response = self.client.post(self.create_url, {
            "name": "product",
            "desc": "desc",
            "price": "11.000"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], "desc")

    def test_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

    def test_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], self.product_data['name'])

    def test_update(self):
        updated_data = {
            "name": "updated product",
            "desc": "desc",
            "price": "50.000"
        }
        response = self.client.put(self.update_url, updated_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], "product")

    def test_delete(self):
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['msg'], "product deleted")