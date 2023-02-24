import datetime
import random
import time
from datetime import date

from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.serializers import LoginSerializer
from dj_rest_auth.views import LoginView
from django.conf import settings
from django.contrib.auth import get_user_model, login, authenticate
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import generics, status, permissions, authentication
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_swagger.views import get_swagger_view

from profile.serializers import FunctionSerializer, ProfileSerializer, UserSerializer, RegisterSerializer, \
    VerifyAccountSerializer, SignUpSerializer, ResendOtpSerializer
from .email import send_email_via_otp
from .models import User, Function, Profile, Otp
import pytz

utc = pytz.UTC


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


schema_view = get_swagger_view(title='Pastebin API')


class Login(LoginView):

    def post(self, request, *args, **kwargs):
        email = request.data.get('username')
        password = request.data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if user:
                login(request, user)
                serialized_user = UserSerializer(user)
                token, created = Token.objects.get_or_create(user=user)
                return Response({'user': serialized_user.data, 'token': token.key})

        return Response({'error': 'Invalid email or password'}, status=400)


class RegisterUserAPIView(RegisterView):
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        user_name_id = data['username']
        serializer = SignUpSerializer(data=data)
        serializer.is_valid()
        serializer.save(request=request)
        user_info = serializer.data
        user_info.update({'password': serializer.cleaned_data['password1']})
        user_id = User.objects.get(username__exact=user_name_id)
        send_email_via_otp(user_name_id, user_id.id)
        return Response({
            'status': 200,
            'message': 'registration successfully check email',
            'user': user_info,
        })


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
            user_exist = User.objects.get(username=username).id
            otp_validate = Otp.objects.get(user_id=user_exist)
            otp_validate.delete()
            send_email_via_otp(username, user_exist)
            return Response({
                'status': 200,
                'message': 'Successfully send Otp',
                'user': serializer.data,
            })


class FunctionListApi(ListAPIView):
    queryset = Function.objects.all()
    serializer_class = FunctionSerializer


class ProfileListApi(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_name(self, profile):
        return profile.name.name


class ProfileRetrieveApi(RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
