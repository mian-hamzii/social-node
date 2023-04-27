from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

from profile.models import Function, Profile, Industry, Domain
from .models import User, Otp

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
    access_token = serializers.CharField(max_length=255, read_only=True)

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'access_token': self.validated_data.get('access_token', ''),
        }

    #
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'access_token']


class UserSerializer(LoginSerializer):
    email = None
    first_name = serializers.CharField(max_length=50)
    id = serializers.IntegerField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'username', 'password']


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
        fields = '__all__'


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    industry = serializers.ReadOnlyField(source='industry.name')
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'industry', 'domain', 'choice_function', 'career_stage', 'Organization_Size',
                  'countries']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSerializer(instance.user).data
        response['industry'] = IndustrySerializer(instance.industry).data['name']
        response['domain'] = DomainSerializer(instance.domain).data['name']
        response['choice_function'] = FunctionSerializer(instance.choice_function).data['name']
        return response
