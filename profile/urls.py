from dj_rest_auth.views import LoginView
from django.urls import path

from . import views
# from .views import CustomAuthToken
from rest_framework.authtoken.views import obtain_auth_token

from .views import RegisterUserAPIView, schema_view

urlpatterns = [
    path('login/', LoginView.as_view(), name='rest_login'),
    path('register/', RegisterUserAPIView.as_view()),
    path("function-list/", views.FunctionListApi.as_view(), name='function'),
    path("profile-list/", views.ProfileListApi.as_view(), name='profile'),
    path("profile-retrieve/<int:pk>", views.ProfileRetrieveApi.as_view(), name='profile-retrieve'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
