from django.urls import path
from .views import PostSituationPublishedAPI, PostSituationDraftAPI, PostSituationDetailPublished, \
    PostSituationDetailDraft, \
    PostSituationUpdateAPI, PostSituationDeleteAPI, InviteAPIView, InvitationResponseAPIView, SituationMatched, \
    PostInviteAPIView

urlpatterns = [
    path('post_situation_published', PostSituationPublishedAPI.as_view()),
    path('post_situation_draft', PostSituationDraftAPI.as_view()),
    path('published_list/', PostSituationDetailPublished.as_view()),
    path('draft_list/', PostSituationDetailDraft.as_view()),
    path('post_situation_update/<int:pk>', PostSituationUpdateAPI.as_view()),
    path('post_situation_delete/<int:pk>', PostSituationDeleteAPI.as_view()),
    path('invite_create', InviteAPIView.as_view()),
    path('invite/<int:request_id>/accept/', InviteAPIView.as_view(), name='invite-update'),
    path('invite_list', InvitationResponseAPIView.as_view()),
    path('post_list', PostInviteAPIView.as_view()),
    path('invitematch_list', SituationMatched.as_view()),
]
