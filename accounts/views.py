import json
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from .models import MyUser
from rest_framework.response import Response

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from .serializers import (MyUserSerializer,
                          MyUserRegistrationSerializer,
                          CustomTokenObtainPairSerializer,
                          PasswordResetConfirmSerializer,
                          PasswordResetRequestSerializer,
                          RegionSerializer)
from .utils import send_activation_email
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.conf import settings
import smtplib

class RegisterView(generics.CreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = MyUserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                
                # Generate token activation
                token = get_random_string(length=32)
                user.activation_token = token
                user.save(update_fields=['activation_token'])

                # Send activation email
                send_activation_email(user.email, token, request.get_host(), email_type="register")

                return Response({
                    "user": serializer.data,
                    "message": "User registered successfully. Please check your email to activate your account.",
                }, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({
                    "message": "An error occurred during registration.",
                    "error": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({
                "message": "Registration failed.",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
class ActivationView(APIView):
    def get(self, request, token, *args, **kwargs):
        try:
            user = MyUser.objects.get(activation_token=token)
            user.is_active = True
            user.activation_token = None
            user.save()
            return Response({'message': 'Account activated successfully.'}, status=status.HTTP_200_OK)
        except MyUser.DoesNotExist:
            return Response({'message': 'Invalid activation token.'}, status=status.HTTP_400_BAD_REQUEST)
        
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            access_token = response.data['access']
            refresh_token = response.data['refresh']

            response.set_cookie(
                'access_token',
                access_token,
                httponly=False,
                secure=False,
                samesite='None',
                max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
                path='/'
            )

            response.set_cookie(
                'refresh_token',
                refresh_token,
                httponly=False,
                secure=False,
                samesite='None',
                max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
                path='/'
            ) 

            response.data.pop('access', None)
            response.data.pop('refresh', None)

            response.data['message'] = 'Login successful'

        return response
        
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            request.data['refresh'] = refresh_token
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            access_token = response.data['access']
            response.set_cookie(
                'access_token',
                access_token,
                httponly=False,
                secure=False,
                samesite='None',
                max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
                path='/'
            )
            response.data.pop('access', None)
            response.data['message'] = 'Token refreshed successfully'
        
        return response

class UsersListView(generics.ListAPIView):
    queryset = MyUser.objects.all().order_by('born_year')
    serializer_class = MyUserSerializer
    permission_classes = (IsAuthenticated,)

class UserInfoView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        serializer = MyUserSerializer(instance=request.user)
        data = serializer.data
        del data['password']
        return Response(data)
    
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            if not refresh_token:
                return Response({"error": "Refresh token not found in cookies."}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            response = Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')

            return response

        except TokenError:
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class PasswordForgotView(generics.CreateAPIView):
    serializer_class = PasswordResetRequestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        
        user = MyUser.objects.filter(email=email).first()
        if user:
            refresh = RefreshToken.for_user(user)
            reset_token = str(refresh.access_token)
            user.reset_code = reset_token
            user.save(update_fields=['reset_code'])
            
            url_path = f"{request.scheme}://{request.get_host()}"
            send_activation_email(user.email, reset_token, domain=url_path, email_type="forgot_pass")
            
            return Response({'detail': 'Password reset token sent successfully.'}, status=status.HTTP_200_OK)
        else:
            # This should not happen due to the validation in the serializer, but it's here as an extra precaution
            return Response({'detail': 'User with this email address does not exist.'}, status=status.HTTP_404_NOT_FOUND)

class PasswordForgotConfirmView(generics.CreateAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        reset_code = serializer.validated_data['reset_code']
        new_password = serializer.validated_data['new_password']
        
        try:
            user = MyUser.objects.get(reset_code=reset_code)
        except MyUser.DoesNotExist:
            return Response({'detail': 'Invalid reset code.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.reset_code = None  # Clear the reset code after use
        user.save()
        
        return Response({'detail': 'Password reset successfully.'}, status=status.HTTP_200_OK)


class GetCountryListView(generics.ListAPIView):
    serializer_class = RegionSerializer

    def get(self, request, *args, **kwargs):
        with open('regions.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        serializer = self.serializer_class(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
    
class GetStateListView(generics.ListAPIView):
    serializer_class = RegionSerializer

    def get(self, request, *args, **kwargs):
        with open('regions.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        country_name = kwargs["country_name"]
        states = next((item['states'] for item in data if item.get('name') == country_name), None)

        if len(states) == 0:
            states = [{"name": country_name}]
        serializer = self.serializer_class(data=states, many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
    
class GetCityListView(generics.ListAPIView):
    serializer_class = RegionSerializer

    def get(self, request, *args, **kwargs):
        with open('regions.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        country_name = kwargs["country_name"]
        state_name = kwargs["state_name"]
        states = next((item['states'] for item in data if item.get('name') == country_name), None)
        cities = next((item['cities'] for item in states if item.get('name') == state_name), None)   
        
        if states == [] and (cities == [] or cities == None):
            states = [{"name": country_name}]
            cities = [{"name": country_name}]

        if states != [] and cities == []:
            cities = [{"name": state_name}]

        serializer = self.serializer_class(data=cities, many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
 
class VerifyTokenView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        access_token = request.COOKIES.get('access_token')

        if not access_token:
            return Response({"error": "No token provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            AccessToken(access_token)
            return Response({"valid": True}, status=status.HTTP_200_OK)
        except TokenError:
            return Response({"valid": False}, status=status.HTTP_400_BAD_REQUEST)
        