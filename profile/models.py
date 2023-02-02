from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.db import models
from django_countries.fields import CountryField


class UserAccountManager(BaseUserManager):
    def create_uer(self, email, username, first_name, last_name, number, password=None):
        if not email:
            raise ValueError('Users must have email address')


class CustomUser(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Otp(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user')
    code = models.CharField(max_length=6)
    created_on = models.DateTimeField(auto_now_add=True)
    expire = models.DateTimeField(auto_now=True)


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

