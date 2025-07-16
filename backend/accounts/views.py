
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from django.shortcuts import render
from django.http import HttpResponse
import os
import mimetypes
from .serializers import UserRegistrationSerializer, LoginSerializer, VoterProfileSerializer, AdminProfileSerializer
from .models import User, VoterProfile, AdminProfile
from django.views.decorators.csrf import csrf_exempt

# HTML Page Views
def login_page(request):
    """Serve the login HTML page"""
    return render(request, 'accounts/Login.html')

def registration_page(request):
    """Serve the registration HTML page"""
    return render(request, 'accounts/registration.html')

def forgot_password_page(request):
    """Serve the forgot password HTML page"""
    return render(request, 'accounts/forgot-password.html')

def reset_password_page(request):
    """Serve the reset password HTML page"""
    return render(request, 'accounts/reset-password.html')

def index_page(request):
    """Serve the index HTML page"""
    return render(request, 'accounts/index.html')

def profile_settings_page(request):
    """Serve the profile settings HTML page"""
    return render(request, 'accounts/profile-settings.html')

def test_connection_page(request):
    """Serve the test connection HTML page"""
    return render(request, 'accounts/test-connection.html')

# API Views (existing code)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'message': 'Registration successful',
            'token': token.key,
            'user_type': user.user_type,
            'user_id': user.id
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        
        # Get user profile data
        profile_data = {}
        if user.user_type == 'voter' and hasattr(user, 'voter_profile'):
            profile_data = VoterProfileSerializer(user.voter_profile).data
        elif user.user_type == 'admin' and hasattr(user, 'admin_profile'):
            profile_data = AdminProfileSerializer(user.admin_profile).data
        
        return Response({
            'message': 'Login successful',
            'token': token.key,
            'user_type': user.user_type,
            'user_id': user.id,
            'profile': profile_data
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        # Delete the user's token
        Token.objects.filter(user=request.user).delete()
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    user = request.user
    
    if user.user_type == 'voter':
        try:
            profile = user.voter_profile
        except VoterProfile.DoesNotExist:
            return Response({'error': 'Voter profile not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if request.method == 'GET':
            serializer = VoterProfileSerializer(profile)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            serializer = VoterProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif user.user_type == 'admin':
        try:
            profile = user.admin_profile
        except AdminProfile.DoesNotExist:
            return Response({'error': 'Admin profile not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if request.method == 'GET':
            serializer = AdminProfileSerializer(profile)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            serializer = AdminProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({'error': 'Invalid user type'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    user = request.user
    profile_data = {}
    
    if user.user_type == 'voter' and hasattr(user, 'voter_profile'):
        profile_data = VoterProfileSerializer(user.voter_profile).data
    elif user.user_type == 'admin' and hasattr(user, 'admin_profile'):
        profile_data = AdminProfileSerializer(user.admin_profile).data
    
    return Response({
        'user_id': user.id,
        'email': user.email,
        'user_type': user.user_type,
        'is_verified': user.is_verified,
        'profile': profile_data
    })
