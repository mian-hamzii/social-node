from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator

from .models import User
from rest_framework import serializers

from profile.models import Function, Profile, Industry, Domain


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2',
                  'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(LoginSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']


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
