from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, PasswordResetView
from django.urls import path

from . import views
# from .views import CustomAuthToken
from rest_framework.authtoken.views import obtain_auth_token

from .views import RegisterUserAPIView, schema_view, VerifyOtp, ResendOtpAPI, ProfileUpdateAPI, Login

urlpatterns = [
    path('login/', Login.as_view(), name='rest_login'),
    path('verify/', VerifyOtp.as_view()),
    path('resend/', ResendOtpAPI.as_view()),
    path('register/', RegisterUserAPIView.as_view()),
    path('reset_password/', PasswordResetView.as_view()),
    path("user_list/", views.UserListApi.as_view(), name='function'),
    path("user_update/", views.UserRetrieveApi.as_view(), name='function'),
    path("profile_list/", views.ProfileListApi.as_view()),
    path("profile_create/", views.ProfileCreateAPI.as_view()),
    path("profile_update/<int:pk>", views.ProfileUpdateAPI.as_view()),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
