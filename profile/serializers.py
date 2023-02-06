from .models import User
from rest_framework import serializers

from profile.models import Function, Profile, Industry, Domain


class CustomUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')
        read_only_fields = ('email',)


class UserSerializer(serializers.ModelSerializer):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'is_active']


class CustomRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone = serializers.IntegerField(required=True)

    def get_cleaned_data(self):
        super().get_cleaned_data()

        return {
            'password' : self.validated_data.get('password',),
            'email' : self.validated_data.get('email',),
            'first_name' : self.validated_data.get('first-name',),
            'last-name' : self.validated_data.get('last_name',),
            'phone' : self.validated_data.get('phone',),
        }


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
