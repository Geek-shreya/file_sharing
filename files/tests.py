import os
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from users.models import CustomUser
from .models import SharedFile

class FileTests(TestCase):
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
        
        # Create a test file
        self.test_file = SimpleUploadedFile(
            "test.docx",
            b"file_content",
            content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        
        # Authenticate OPS user
        ops_login = self.client.post(reverse('login'), {
            'username': 'opsuser',
            'password': 'testpass123'
        })
        self.ops_token = ops_login.data['token']
        
        # Authenticate Client user
        client_login = self.client.post(reverse('login'), {
            'username': 'clientuser',
            'password': 'testpass123'
        })
        self.client_token = client_login.data['token']
    
    def test_file_upload_by_ops(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.ops_token}')
        url = reverse('file-upload')
        data = {'file': self.test_file}
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SharedFile.objects.count(), 1)
    
    def test_file_upload_by_client(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.client_token}')
        url = reverse('file-upload')
        data = {'file': self.test_file}
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_file_list(self):
        # First upload a file
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.ops_token}')
        upload_url = reverse('file-upload')
        self.client.post(upload_url, {'file': self.test_file}, format='multipart')
        
        # Now test listing
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.client_token}')
        list_url = reverse('file-list')
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_file_download(self):
        # First upload a file
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.ops_token}')
        upload_url = reverse('file-upload')
        upload_response = self.client.post(upload_url, {'file': self.test_file}, format='multipart')
        file_id = upload_response.data['id']
        
        # Request download link
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.client_token}')
        download_url = reverse('file-download')
        response = self.client.post(download_url, {'file_id': file_id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('download_url', response.data)
        
        # Try to download the file
        download_link = response.data['download_url']
        response = self.client.get(download_link)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_file_download_by_non_client(self):
        # First upload a file
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.ops_token}')
        upload_url = reverse('file-upload')
        upload_response = self.client.post(upload_url, {'file': self.test_file}, format='multipart')
        file_id = upload_response.data['id']
        
        # Request download link as client
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.client_token}')
        download_url = reverse('file-download')
        response = self.client.post(download_url, {'file_id': file_id}, format='json')
        download_link = response.data['download_url']
        
        # Now try to download as OPS user (should fail)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.ops_token}')
        response = self.client.get(download_link)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)