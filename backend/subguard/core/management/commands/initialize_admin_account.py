import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create initial admin account"

    def handle(self, *args, **options) -> None:
        DJANGO_ADMIN_EMAIL: str | None = os.environ.get("DJANGO_ADMIN_EMAIL")
        DJANGO_ADMIN_PASSWORD: str | None = os.environ.get("DJANGO_ADMIN_PASSWORD")

        if None in (DJANGO_ADMIN_EMAIL, DJANGO_ADMIN_PASSWORD):
            self.stdout.write(
                self.style.WARNING(
                    "Missing environemntal credentials. Skipping `initialize_admin_account` command."
                )
            )
            return

        User = get_user_model()
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(
                self.style.WARNING(
                    "Admin account already exist. Skipping `initialize_admin_account` command."
                )
            )
            return

        User.objects.create_superuser(
            email=DJANGO_ADMIN_EMAIL,
            password=DJANGO_ADMIN_PASSWORD
        )

        self.stdout.write(self.style.SUCCESS("Successfully initialize admin account."))


