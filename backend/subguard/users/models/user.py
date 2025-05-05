import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from users.managers import UserManager


class User(AbstractUser):

    username = None

    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    email = models.EmailField(verbose_name="email address", db_index=True, unique=True)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self) -> str:
        return f"User(id='{self.id}', email='{self.email}')"