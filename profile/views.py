from django.contrib.auth.models import User
from rest_framework import authentication, permissions
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

# from profile.serializers import UserSerializer

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from profile.models import Function, Profile, CustomUser
from profile.serializers import FunctionSerializer, ProfileSerializer, UserSerializer


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UserApi(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]


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

# class UserList(RetrieveAPIView):
#     # queryset = Profile.objects.all()
#     # serializer_class = UserSerializer
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticatedOrReadOnly]


# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# class CustomAuthToken(ObtainAuthToken):
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data,
#                                            context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({
#             'token': token.key,
#             'user_id': user.pk,
#             'email': user.email
#         })
