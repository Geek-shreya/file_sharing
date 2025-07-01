from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import CustomUser

class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.ops_user = CustomUser.objects.create_user(
            username='opsuser',
            email='ops@example.com',
            password='testpass123',
            user_type='OPS'
        )
        self.client_user = CustomUser.objects.create_user(
            username='clientuser',
            email='client@example.com',
            password='testpass123',
            user_type='CLIENT',
            is_verified=True
        )
    
    def test_register_ops_user(self):
        url = reverse('register')
        data = {
            'username': 'newops',
            'email': 'newops@example.com',
            'password': 'testpass123',
            'user_type': 'OPS'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CustomUser.objects.count(), 3)
    
    def test_register_client_user(self):
        url = reverse('register')
        data = {
            'username': 'newclient',
            'email': 'newclient@example.com',
            'password': 'testpass123',
            'user_type': 'CLIENT'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CustomUser.objects.count(), 3)
        self.assertIn('Verification email sent', response.data['message'])
    
    def test_login_ops_user(self):
        url = reverse('login')
        data = {
            'username': 'opsuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
    
    def test_login_client_user(self):
        url = reverse('login')
        data = {
            'username': 'clientuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
    
    def test_login_unverified_client_user(self):
        unverified_client = CustomUser.objects.create_user(
            username='unverified',
            email='unverified@example.com',
            password='testpass123',
            user_type='CLIENT',
            is_verified=False
        )
        url = reverse('login')
        data = {
            'username': 'unverified',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Email not verified')