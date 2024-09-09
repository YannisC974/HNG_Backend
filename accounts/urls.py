from django.urls import path
from .views import (RegisterView,
                    UsersListView,
                    CustomTokenObtainPairView,
                    ActivationView,
                    LogoutView,
                    PasswordForgotView,
                    PasswordForgotConfirmView,
                    GetCountryListView,
                    GetStateListView,
                    GetCityListView,
                    UserInfoView,
                    CustomTokenRefreshView,
                    VerifyTokenView
                    )


app_name = "accounts"
urlpatterns = [
    path("list/", UsersListView.as_view(), name="list"), 
    path("user-info/", UserInfoView.as_view(), name="user-info"), 
    
    path("register/", RegisterView.as_view(), name="register"), 
    path("activate/<str:token>/", ActivationView.as_view(), name="activate"),

    path('login/', CustomTokenObtainPairView.as_view(), name='login'), 
    path("verify-token/", VerifyTokenView.as_view(), name="verify"),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'), 
    path('logout/', LogoutView.as_view(), name='logout'), 
    path('password-forgot/', PasswordForgotView.as_view(), name='password-forgot'),
    path('password-forgot-confirm/<str:reset_token>/', PasswordForgotConfirmView.as_view(), name='password-forgot-confirm'),
    path('get-countries/', GetCountryListView.as_view(), name='get-countries'),
    path('get-states/<country_name>/', GetStateListView.as_view(), name='get-states'),
    path('get-cities/<country_name>/<state_name>/', GetCityListView.as_view(), name='get-cities'),
]
