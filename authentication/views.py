from django.shortcuts import get_object_or_404
from .models import User,Candidate,CustomToken,Recruiter
from .serializers import UserSerializer,CandidateSerializer,RecruiterSerializer
from rest_framework.decorators import api_view ,authentication_classes,permission_classes
from rest_framework.response import Response 
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ValidationError
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils import timezone
from django.contrib.auth import authenticate, login
from datetime import timedelta
from dotenv import load_dotenv
import os
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenRefreshView

@api_view(['POST'])
def user_login(request):
    email = request.data.get('email')
    password = request.data.get('password')

  
    user = authenticate(email=email, password=password)

    if user is None:
        return Response({"detail": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
    if not user.is_active:
        return Response({"detail": "Your account is not active, please verify your email address"}, status=status.HTTP_401_UNAUTHORIZED)
   
    # log the user into the current session
    login(request, user)

    # Generate tokens
    refresh = RefreshToken.for_user(user)
    access = AccessToken.for_user(user)

    return Response({
        "access_token": str(access),
        "refresh_token": str(refresh),
        "status": status.HTTP_200_OK,
        "user": UserSerializer(instance=user).data
    })



class CustomTokenRefreshView(TokenRefreshView):
    pass


@api_view(['POST'])
def signup(request):
    type = request.data.get('type')

    if type == 'candidate':
        serializer = CandidateSerializer(data=request.data)
        model = Candidate

    elif type == 'recruiter':
        serializer = RecruiterSerializer(data=request.data)
        model = Recruiter

    else:
        return Response({"error": "Invalid user type"}, status=status.HTTP_400_BAD_REQUEST)

    if serializer.is_valid(raise_exception=True):
        email = request.data.get('email')

        if model.objects.filter(email=email).exists():
            return Response({"error": "A user with this email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        user.set_password(request.data['password'])
        user.is_active = False
        user.save()

        token = default_token_generator.make_token(user)
        expiration_time = timezone.now() + timezone.timedelta(minutes=15)
        CustomToken.objects.create(user=user, token=token, expiration_date=expiration_time)

        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        load_dotenv()
        reset_password = os.getenv('PULS_DIGITAL')

        verification_url = f"{reset_password}{uidb64}/{token}/"
      

        subject = 'Verify your email address'
        message = f'Click the following link to verify your email address: <a href="{verification_url}">click</a>'
        send_mail(subject, None, None, [email], None, None, None, None, message)
        
        return Response({"message": "Verification email sent"}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def email_verified(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return Response({'error': 'Invalid user'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        custom_token = CustomToken.objects.get(user=user, token=token)
    except CustomToken.DoesNotExist:
        return Response({'error': 'Invalid verification link'}, status=status.HTTP_400_BAD_REQUEST)
        
    if timezone.now() > custom_token.expiration_date:
        return Response({'error': 'Verification link has expired'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        user.is_active = True
        user.save()
        custom_token.delete()
        
        return Response({'message': 'Email successfully verified'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def reset_password(request):
    email = request.data.get('email')

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    # Generate and save token with expiration time
    token = default_token_generator.make_token(user)
    expiration_time = timezone.now() + timedelta(minutes=15)
    CustomToken.objects.create(user=user, token=token, expiration_date=expiration_time)
    
    # Generate password reset URL
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

    load_dotenv()
    print(os.getenv("RESETED_PASSWORD"))
    reset_password = os.getenv('RESETED_PASSWORD')

    verification_url = f"{reset_password}{uidb64}/{token}/"

    # Send verification email
    subject = 'Reset Your Password'
    
    message = f'Click the following link to reset your password: <a href="{verification_url}">click</a>'

    recipient_email = user.email
    
    send_mail(subject, None, None, [recipient_email], None, None, None, None, message)
    
    return Response({"message": "Check your email for password reset instructions"}, status=status.HTTP_200_OK)


@api_view(['POST'])
def reseted_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return Response({'error': 'Invalid user'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        custom_token = CustomToken.objects.get(user=user, token=token)
    except CustomToken.DoesNotExist:
        return Response({'error': 'Invalid verification link'}, status=status.HTTP_400_BAD_REQUEST)
        
    if timezone.now() > custom_token.expiration_date:
        return Response({'error': 'Verification link has expired'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        new_password = request.data.get('new_password')
        if not new_password:
            return Response({'error': 'New password not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        custom_token.delete()
        
        return Response({'message': 'Password successfully reset'}, status=status.HTTP_200_OK)
    


    
