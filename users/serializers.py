from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser
from rest_framework.exceptions import AuthenticationFailed

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'user_type')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'user_type')
        extra_kwargs = {
            'user_type': {'required': True}
        }
    
    def validate_user_type(self, value):
        if value not in ['OPS', 'CLIENT']:
            raise serializers.ValidationError("Invalid user type")
        return value
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            user_type=validated_data['user_type']
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise AuthenticationFailed('Invalid credentials')
        if not user.is_active:
            raise AuthenticationFailed('User account is disabled')
        if user.user_type == 'CLIENT' and not user.is_verified:
            raise AuthenticationFailed('Email not verified')
        return user

class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.CharField()