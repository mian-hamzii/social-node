import datetime

import pytz
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, PasswordResetView
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.db.models import Q, Prefetch
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView, CreateAPIView, get_object_or_404, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_swagger.views import get_swagger_view

from profile.serializers import ProfileSerializer, UserSerializer, VerifyAccountSerializer, SignUpSerializer, \
    ResendOtpSerializer
from situation.models import Invite
from .email import send_email_via_otp
from .models import User, Profile, Otp, Industry

utc = pytz.UTC


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


schema_view = get_swagger_view(title='Pastebin API')


class RegisterUserAPIView(RegisterView):
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        send_email_via_otp(user, user.id)
        return user


class VerifyOtp(APIView):
    serializer_class = VerifyAccountSerializer
    permission_classes = (AllowAny,)

    def post(self, request):

        data = request.data
        serializer = VerifyAccountSerializer(data=data)
        if serializer.is_valid():
            username = serializer.data['username']
            otp = serializer.data['otp']
            user_exist = User.objects.filter(username=username).first()
            if not user_exist:
                return Response({
                    'status': 400,
                    'message': 'something went wrong',
                    'data': 'invalid email'
                })

            otp_validate = Otp.objects.filter(user_id=user_exist.id).first()
            otp_code = otp_validate.code

            if otp_code != otp:
                return Response({
                    'status': 400,
                    'message': 'something went wrong',
                    'data': 'wrong otp'
                })
            if otp_code:
                if otp_validate.expire > utc.localize(datetime.datetime.now()):
                    return Response({
                        'status': 200,
                        'message': 'account verified',
                        'data': serializer.data,
                    })
                if otp_validate.expire < utc.localize(datetime.datetime.now()):
                    return Response({
                        'message': 'Otp Expired'
                    })


class ResendOtpAPI(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ResendOtpSerializer

    def post(self, request):
        data = request.data
        serializer = ResendOtpSerializer(data=data)
        if serializer.is_valid():
            username = serializer.data['username']
            user_exist = User.objects.filter(username=username).first()
            if not user_exist:
                return Response({
                    'status': 400,
                    'message': 'something went wrong',
                    'data': 'invalid email'
                })
            otp_validate = Otp.objects.filter(user_id=user_exist.id).first()
            otp_validate.delete()
            send_email_via_otp(username, user_exist.id)
            return Response({
                'status': 200,
                'message': 'Successfully send Otp',
                'user': serializer.data,
            })


class UserListApi(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = User.objects.filter(Q(profile__domain=self.request.user.profile_set.first().domain) |
                                   Q(profile__choice_function=self.request.user.profile_set.first().choice_function) |
                                   Q(profile__career_stage=self.request.user.profile_set.first().career_stage) |
                                   Q(profile__Organization_Size=self.request.user.profile_set.first().Organization_Size)
                                   ).exclude(profile__user=self.request.user)
        serializer1 = self.serializer_class(user, many=True)
        Serializer_list = [serializer1.data]
        return Response(Serializer_list)


class UserRetrieveApi(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ProfileCreateAPI(CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        industry = get_object_or_404(Industry, domain=self.request.data['domain'])
        return serializer.save(industry=industry, user=self.request.user)


class ProfileListApi(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_name(self, profile):
        return profile.name.name

    def get_queryset(self):
        return Profile.objects.filter(user__profile=self.request.user.profile_set.first())


class ProfileUpdateAPI(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
