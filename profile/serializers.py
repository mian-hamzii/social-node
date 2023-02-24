from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from .models import User, Otp
from rest_framework import serializers
from profile.models import Function, Profile, Industry, Domain
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import SetPasswordForm, PasswordResetForm
from django.urls import exceptions as url_exceptions
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, serializers
from rest_framework.exceptions import ValidationError

# Get the UserModel
UserModel = get_user_model()


class SignUpSerializer(RegisterSerializer):
    # username = serializers.EmailField(
    #     required=True,
    #     validators=[UniqueValidator(queryset=User.objects.all())]
    # )
    email = None
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
        }

    #
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']


class UserSerializer(LoginSerializer):
    email = None

    class Meta:
        model = User
        fields = ['username', 'password']


class VerifyAccountSerializer(serializers.Serializer):
    username = serializers.CharField()
    otp = serializers.CharField(max_length=10)


class ResendOtpSerializer(serializers.Serializer):
    username = serializers.CharField()


class OtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = ['code']


class FunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Function
        fields = ['id', 'name']


class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = ['id', 'name']


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ['id', 'name']


class ProfileSerializer(serializers.ModelSerializer):
    industry = IndustrySerializer()
    domain = DomainSerializer()
    function = FunctionSerializer()

    class Meta:
        model = Profile
        fields = ['industry', 'domain', 'function', 'career_stage', 'Organization_Size', 'countries']
