from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser, UserManager
from django.db.models import Manager
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django_countries.fields import CountryField


class User(AbstractUser):
    username = models.EmailField(unique=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def name(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.username


class Otp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    code = models.CharField(max_length=6)
    created_on = models.DateTimeField(auto_now_add=True)
    expire = models.DateTimeField()


class Industry(models.Model):
    name = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Domain(models.Model):
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Function(models.Model):
    name = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


CHOICE = (
    ("Choose Career Stage", "Choose Career Stage"),
    ("Entry Level", "Entry Level"),
    ("Junior Level", "Junior Level"),
    ("Middle Level", "Middle Level"),
    ("Senior Level", "Senior Level"),
)

CHOICES = (
    ("Organization Size", "Organization Size"),
    ("Entry Level", "Entry Level"),
    ("Junior Level", "Junior Level"),
    ("Middle Level", "Middle Level"),
    ("Senior Level", "Senior Level"),
)


class Profile(models.Model):
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, null=True, blank=True)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    function = models.ForeignKey(Function, on_delete=models.CASCADE)
    career_stage = models.CharField(max_length=25, choices=CHOICE, default='Choose Career Stage')
    Organization_Size = models.CharField(max_length=25, choices=CHOICES, default='Organization Size')
    countries = CountryField()
    verify = models.BooleanField(default=False)
