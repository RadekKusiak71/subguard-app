from typing import TYPE_CHECKING, Any, Dict

from django.contrib.auth.models import BaseUserManager

if TYPE_CHECKING:
    from users.models import User


class UserManager(BaseUserManager):

    def create_user(self, email: str, password: str, **extra_fields: Dict[str, Any]) -> 'User':
        if not email:
            raise ValueError("The given email must be set")

        email: str = self.normalize_email(email)
        user: User = self.model(email=email, **extra_fields)
        user.set_password(raw_password=password)
        user.save()
        return user

    def create_superuser(self, email: str, password: str, **extra_fields: Dict[str, Any]) -> 'User':
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email=email, password=password, **extra_fields)
