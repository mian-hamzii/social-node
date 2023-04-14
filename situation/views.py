import requests
from django.http import JsonResponse, Http404, HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView, RetrieveUpdateAPIView, \
    ListCreateAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from profile.models import User
from profile.serializers import UserSerializer
from situation.models import PostSituation, Invite
from situation.serializers import PostSituationSerializer, InviteSerializer, PostMatchSerializer


class PostSituationPublishedAPI(CreateAPIView):
    queryset = PostSituation.objects.all()
    serializer_class = PostSituationSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, status='published')


class PostSituationDraftAPI(CreateAPIView):
    queryset = PostSituation.objects.all()
    serializer_class = PostSituationSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, status='draft')


class PostSituationDetailPublished(ListAPIView):
    queryset = PostSituation.objects.all()
    serializer_class = PostSituationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return PostSituation.objects.filter(user_id=self.request.user.id, status='published')


class PostSituationDetailDraft(ListAPIView):
    queryset = PostSituation.objects.all()
    serializer_class = PostSituationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return PostSituation.objects.filter(user_id=self.request.user.id, status='draft')


class PostSituationUpdateAPI(RetrieveUpdateAPIView):
    queryset = PostSituation.objects.all()
    serializer_class = PostMatchSerializer
    permission_classes = (permissions.AllowAny,)


class PostSituationDeleteAPI(DestroyAPIView):
    queryset = PostSituation.objects.all()
    serializer_class = PostSituationSerializer
    permission_classes = (AllowAny,)


class InviteAPIView(APIView):
    serializer_class = InviteSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data
        receiver_id = request.data.get('user_id')
        post_id = request.data.get('post_id')
        # if receiver_id is None:
        #     return Response({'error': 'friend_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        # if receiver_id == request.user.id:
        #     return Response({'error': 'You cannot send a friend request to yourself'},
        #                     status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=data)
        if receiver_id:
            if serializer.is_valid():
                receiver = User.objects.get(id=receiver_id)
                post_situation = self.request.user.postsituation_set.first()
                invite = Invite(question_id=post_situation, user=receiver, status='invited')
                invite.save()
                if post_situation:
                    data = {'question_id': post_situation.id, 'user': receiver.id}
                    return Response({'status': 'Friend request sent successfully', 'data': data})
                else:
                    return Response({'status': 'No object'})
        if post_id:
            if serializer.is_valid():
                user = self.request.user
                post = PostSituation.objects.filter(id=post_id).first()
                invite = Invite(question_id=post, user=user, status='willing to advised')
                invite.save()

                if post:
                    data = {'question_id': post.id, 'user': user.id}
                    return Response({'status': 'Request successful', 'data': data})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        request_id = kwargs.get('request_id')
        if request_id is None:
            return Response({'error': 'request_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            receiver = User.objects.get(receiver=request_id)
            post_situation = self.request.user.postsituation_set.first()
            friend_request = Invite.objects.get(receiver=receiver)
        except Invite.DoesNotExist:
            return Response({'error': 'Invalid request_id'}, status=status.HTTP_400_BAD_REQUEST)
        friend_request.accept()
        return Response({'status': 'Friend request accepted successfully'})


class InviteUpdateAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Invite.objects.all()
    serializer_class = InviteSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        friend_request = self.get_object()
        friend_request.accept()

    def delete(self, request, *args, **kwargs):
        friend_request = self.get_object()
        friend_request.reject()


class InvitationResponseAPIView(ListAPIView):
    serializer_class = InviteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        invite = Invite.objects.filter(question_id__user=user, status='invited')
        return invite


class PostInviteAPIView(ListAPIView):
    serializer_class = InviteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        post_invite = Invite.objects.filter(user=user, status='willing to advised')
        return post_invite


class SituationMatched(ListAPIView):
    serializer_class = PostMatchSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        domain = user.profile_set.first().domain
        posts = PostSituation.objects.filter(user__profile__domain=domain).exclude(user=user)
        return posts
