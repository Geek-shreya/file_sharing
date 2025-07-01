from rest_framework import serializers
from .models import SharedFile, FileShareLink
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

class SharedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedFile
        fields = ('id', 'original_filename', 'uploaded_at', 'uploader')
        read_only_fields = ('id', 'original_filename', 'uploaded_at', 'uploader')

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedFile
        fields = ('file',)
    
    def validate(self, data):
        user = self.context['request'].user
        if user.user_type != 'OPS':
            raise serializers.ValidationError("Only operation users can upload files")
        return data

class FileShareLinkSerializer(serializers.ModelSerializer):
    download_url = serializers.SerializerMethodField()
    
    class Meta:
        model = FileShareLink
        fields = ('download_url', 'expires_at')
    
    def get_download_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(f'/api/download-file/{obj.token}/')

class FileDownloadSerializer(serializers.Serializer):
    file_id = serializers.IntegerField()