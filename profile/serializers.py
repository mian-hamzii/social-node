from django.contrib.auth.models import User
from rest_framework import serializers

from profile.models import Function, Profile, Industry, Domain, CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'number']


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
