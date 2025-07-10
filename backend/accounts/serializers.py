
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, VoterProfile, AdminProfile

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    student_id = serializers.CharField()
    department = serializers.CharField()
    phone_number = serializers.CharField(required=False)
    date_of_birth = serializers.DateField(required=False)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'confirm_password', 
                 'first_name', 'last_name', 'student_id', 'department', 
                 'phone_number', 'date_of_birth']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords don't match.")
        return attrs
    
    def create(self, validated_data):
        # Remove confirm_password and profile fields
        profile_data = {
            'first_name': validated_data.pop('first_name'),
            'last_name': validated_data.pop('last_name'),
            'student_id': validated_data.pop('student_id'),
            'department': validated_data.pop('department'),
            'phone_number': validated_data.pop('phone_number', ''),
            'date_of_birth': validated_data.pop('date_of_birth', None),
        }
        validated_data.pop('confirm_password')
        
        # Create user
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            user_type='voter'
        )
        
        # Create voter profile
        VoterProfile.objects.create(user=user, **profile_data)
        
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    user_type = serializers.ChoiceField(choices=['voter', 'admin'])
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user_type = attrs.get('user_type')
        
        if email and password:
            user = authenticate(username=email, password=password)
            
            if user:
                if not user.is_active:
                    raise serializers.ValidationError('User account is disabled.')
                
                if user.user_type != user_type:
                    raise serializers.ValidationError('Invalid user type.')
                
                attrs['user'] = user
                return attrs
            else:
                raise serializers.ValidationError('Invalid login credentials.')
        else:
            raise serializers.ValidationError('Must include email and password.')

class VoterProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = VoterProfile
        fields = ['first_name', 'last_name', 'student_id', 'department', 
                 'phone_number', 'date_of_birth', 'profile_image', 'email']

class AdminProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = AdminProfile
        fields = ['first_name', 'last_name', 'role', 'department', 
                 'profile_image', 'email']
