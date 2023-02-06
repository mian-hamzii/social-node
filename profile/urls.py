from django.urls import path
from . import views
# from .views import CustomAuthToken
from rest_framework.authtoken.views import obtain_auth_token

from .views import GenericUserAPIView, UserAPIView, CustomRegisterView

urlpatterns = [
    path('users/', UserAPIView.as_view()),
    path('user/<int:id>', GenericUserAPIView.as_view()),
    path('register/', CustomRegisterView.as_view()),
    # path("user-list/", views.UserApi.as_view(), name='user-list'),
    path("function-list/", views.FunctionListApi.as_view(), name='function'),
    path("profile-list/", views.ProfileListApi.as_view(), name='profile'),
    path("profile-retrieve/<int:pk>", views.ProfileRetrieveApi.as_view(), name='profile-retrieve'),
    # path("users/<int:pk>", views.UserDetail.as_view(), name='user_detail'),
    # path('api-token-auth/', CustomAuthToken.as_view()),
    # path('gettoken/', obtain_auth_token)
]
