import datetime
import random
import smtplib
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from profile.models import Otp


def send_email_via_otp(username, id):
    subject = 'Your account verification email'
    otp = random.randint(100000, 999999)
    expire = timezone.now() + datetime.timedelta(minutes=10)
    message = f'Your otp in {otp}'
    from_email = settings.EMAIL_HOST
    send_mail(subject, message, from_email, [username])
    otp_obj = Otp(code=otp, user_id=id, expire=expire)
    otp_obj.save()
