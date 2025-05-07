import uuid
from datetime import datetime, timedelta

from django.db import models
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def get_expire_date() -> datetime:
    return timezone.now() + timedelta(minutes=15)


class UserVerfication(models.Model):

    id = models.UUIDField(primary_key=True, unique=True, editable=True, default=uuid.uuid4)
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="user_verifications")
    expires_at = models.DateTimeField(default=get_expire_date)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"UserVerification(id='{self.id}', email='{self.user.email}')"

    @property
    def is_expired(self) -> bool:
        return self.expires_at < timezone.now()

    def send_verification_email(self) -> None:
        html_content: str = render_to_string("verify_email.html", {
            "verification_link": f'{settings.DJANGO_EMAIL_VERIFICATION_LINK}/{self.id}'
        })
        email: EmailMultiAlternatives = EmailMultiAlternatives(subject="Verify Your Account - SubGuard", body="", to=[self.user.email])
        email.attach_alternative(html_content, "text/html")
        email.send()