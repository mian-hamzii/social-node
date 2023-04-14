from django.db import models

from profile.models import User

CHOICE = (
    ("$5", "$5"),
    ("$10", "$10"),
)
CHOICES = (
    ("invited", "invited"),
    ("willing to advised", "willing to advised"),
    ("accepted", "accepted"),
)
DRAFT = 'draft'
PUBLISHED = 'published'
STATUS_CHOICE = ((DRAFT, 'Save Draft'), (PUBLISHED, 'Published'))


class PostSituation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=45)
    description = models.TextField()
    price = models.CharField(max_length=15, choices=CHOICE)
    valid_time = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, default=DRAFT, choices=STATUS_CHOICE)

    def __str__(self):
        return self.title


class Invite(models.Model):
    question_id = models.ForeignKey(PostSituation, on_delete=models.CASCADE, null=True, blank=True,
                                    related_name='question_id')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='receiver')
    status = models.CharField(max_length=50, choices=CHOICES, default='invite')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def accept(self):
        self.status = 'accepted'
        self.save()

    def reject(self):
        self.status = 'rejected'
        self.save()
