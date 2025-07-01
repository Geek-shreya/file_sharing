from django.urls import path, include
from rest_framework import routers
from users.views import RegisterAPI, LoginAPI, VerifyEmailAPI, UserAPI
from files.views import FileUploadAPI, FileListAPI, FileDownloadAPI, SecureFileDownloadAPI

urlpatterns = [
    # Auth URLs
    path('auth/register/', RegisterAPI.as_view(), name='register'),
    path('auth/login/', LoginAPI.as_view(), name='login'),
    path('auth/verify-email/', VerifyEmailAPI.as_view(), name='verify-email'),
    path('auth/user/', UserAPI.as_view(), name='user'),
    
    # File URLs
    path('files/upload/', FileUploadAPI.as_view(), name='file-upload'),
    path('files/list/', FileListAPI.as_view(), name='file-list'),
    path('files/download/', FileDownloadAPI.as_view(), name='file-download'),
    path('download-file/<str:token>/', SecureFileDownloadAPI.as_view(), name='secure-file-download'),
]