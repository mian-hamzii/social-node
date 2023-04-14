from rest_framework import serializers

from profile.models import User
from profile.serializers import UserSerializer
from situation.models import PostSituation, Invite


class PostSituationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostSituation
        fields = ['id', 'user', 'title', 'description', 'price', 'valid_time', 'status']
        read_only_fields = ('user',)


class PostMatchSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = PostSituation
        fields = ['id', 'user', 'title', 'description', 'price', 'valid_time']


class InviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invite
        fields = ['id', 'user', 'question_id', 'status', 'created_at', 'modified_at']
