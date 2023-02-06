from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_auth.registration.views import RegisterView
from rest_framework import generics
from rest_framework import mixins
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from profile.serializers import UserSerializer, FunctionSerializer, ProfileSerializer
from .models import User, Function, Profile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class CustomRegisterView(RegisterView):
    queryset = User.objects.all()


class UserAPIView(APIView):
    @staticmethod
    def get(requests):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class GenericUserAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin,
                         mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    lookup_field = 'id'

    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)


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
