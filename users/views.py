from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, EmailVerificationSerializer
from .models import CustomUser
from django.core.mail import send_mail
from django.conf import settings

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        message = "User created successfully."
        email_sent = False
        
        if user.user_type == 'CLIENT':
            try:
                # Generate verification link
                verification_link = f"{settings.FRONTEND_URL}/verify-email?token={user.verification_token}"
                
                # Send verification email
                send_mail(
                    subject='Verify your email',
                    message=f'Click the link to verify your email: {verification_link}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                email_sent = True
                message = "User created successfully. Verification email sent."
            except Exception as e:
                # Log the error but continue
                print(f"Error sending verification email: {str(e)}")
                message = "User created successfully. Could not send verification email."
        
        # Always return token regardless of email success
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1],
            "message": message,
            "email_sent": email_sent,  # For debugging
            "verification_token": user.verification_token if user.user_type == 'CLIENT' else None
        }, status=status.HTTP_201_CREATED)

class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

class VerifyEmailAPI(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        token = serializer.validated_data['token']
        try:
            user = CustomUser.objects.get(verification_token=token, is_verified=False)
            user.is_verified = True
            user.save()
            return Response({"message": "Email verified successfully"})
        except CustomUser.DoesNotExist:
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user