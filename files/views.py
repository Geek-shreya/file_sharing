import os
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.crypto import get_random_string
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from .models import SharedFile, FileShareLink
from .serializers import (
    SharedFileSerializer, 
    FileUploadSerializer,
    FileShareLinkSerializer,
    FileDownloadSerializer
)
from users.models import CustomUser

class FileUploadAPI(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FileUploadSerializer
    
    def perform_create(self, serializer):
        if self.request.user.user_type != 'OPS':
            return Response(
                {"error": "Only operation users can upload files"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        file_obj = serializer.save(
            uploader=self.request.user,
            original_filename=self.request.FILES['file'].name
        )
        return file_obj

class FileListAPI(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SharedFileSerializer
    
    def get_queryset(self):
        return SharedFile.objects.all().order_by('-uploaded_at')

class FileDownloadAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = FileDownloadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        file_id = serializer.validated_data['file_id']
        shared_file = get_object_or_404(SharedFile, id=file_id)
        
        # Create a share link
        token = get_random_string(50)
        share_link = FileShareLink.objects.create(
            file=shared_file,
            token=token,
            expires_at=None  # Link doesn't expire
        )
        
        serializer = FileShareLinkSerializer(
            share_link,
            context={'request': request}
        )
        
        return Response(serializer.data)

class SecureFileDownloadAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, token, *args, **kwargs):
        share_link = get_object_or_404(FileShareLink, token=token)
        
        # Check if the current user is a client user
        if request.user.user_type != 'CLIENT':
            return Response(
                {"error": "Only client users can download files"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        file_path = share_link.file.file.path
        if not os.path.exists(file_path):
            raise Http404("File not found")
        
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{share_link.file.original_filename}"'
        return response