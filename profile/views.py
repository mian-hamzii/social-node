from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_auth.registration.views import RegisterView
from rest_framework import generics
from rest_framework import mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from profile.serializers import UserSerializer, FunctionSerializer, ProfileSerializer, RegisterSerializer
from .models import User, Function, Profile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(requests):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class CreateUserApi(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RegisterUserAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
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
