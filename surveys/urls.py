from django.urls import path
from .views import *

app_name = "surveys"
urlpatterns = [
    path("create/", UserSurveyViewSet.as_view({'post': 'create'}), name="create"),
    path('choose-user-survey/<str:day>/', RandomUserSurveyChooseView.as_view(), name='choose-user-survey'),
    path('update-user-survey-validation/<int:pk>/', UpdateUserSurveyValidationView.as_view(), name='update-user-survey-validation'),
]

