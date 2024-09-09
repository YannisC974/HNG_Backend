from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import MyUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        
        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)

            if not user:
                raise serializers.ValidationError('No active account found with the given credentials')
            
            self.user = user
        else:
            raise serializers.ValidationError('Must include "email" and "password".')

        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)  

        return data

class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'email', 'username', 'auth_provider', 'slug', 'born_year', 
                  'gender', 'is_student', 'university_name', 'country', 'state', 
                  'city', 'is_active', 'current_active_days', 'max_consecutive_active_days']
        read_only_fields = ['id', 'slug', 'is_active']

class MyUserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = MyUser
        fields = ['email', 'username', 'password', 'password2', 'born_year', 'gender', 'is_student', 
                  'university_name', 'country', 'state', 'city']
        extra_kwargs = {
            'born_year': {'required': False},
            'gender': {'required': False},
            'is_student': {'required': False},
            'university_name': {'required': False},
            'country': {'required': False},
            'state': {'required': False},
            'city': {'required': False},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        # Verify if username already exists
        if MyUser.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({"username": "A user with that username already exists."})
        
        # Verify if email already exists
        if MyUser.objects.filter(username=attrs['email']).exists():
            raise serializers.ValidationError({"email": "This e-mail has already been registered."})
        
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        return MyUser.objects.create_user(**validated_data)

class MyUserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = MyUser.objects.get(email=obj['email'])
        return user.tokens()

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = MyUser.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError('Invalid credentials, try again')
        if not user.check_password(password):
            raise serializers.ValidationError('Invalid credentials, try again')
        if not user.is_active:
            raise serializers.ValidationError('Account is not active, please check your email')
        return attrs

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not MyUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email address does not exist.")
        return value

class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    new_password2 = serializers.CharField(write_only=True)
    reset_code = serializers.CharField()

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs

class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct")
        return value
    
class RegionSerializer(serializers.Serializer):
    name = serializers.CharField()