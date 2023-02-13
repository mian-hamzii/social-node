from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import generics, status, permissions, authentication
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_swagger.views import get_swagger_view

from profile.serializers import FunctionSerializer, ProfileSerializer, RegisterSerializer, UserSerializer
from .models import User, Function, Profile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


schema_view = get_swagger_view(title='Pastebin API')


class UserAPI(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        is_registered = User.objects.filter(email=request.data.get('email'), password=request.data.get('password')).exists()
        content = {
            # 'email': request.data.get('email'),  # `django.contrib.auth.User` instance.
            # 'password': request.data.get('password'),  # `django.contrib.auth.User` instance.
            "valid_user": is_registered
        }
        return Response(content)


class RegisterUserAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class FunctionListApi(ListAPIView):
    queryset = Function.objects.all()
    serializer_class = FunctionSerializer


# authentication_classes = [authentication.TokenAuthentication]
# permission_classes = [permissions.IsAdminUser]


class ProfileListApi(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_name(self, profile):
        return profile.name.name


class ProfileRetrieveApi(RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
