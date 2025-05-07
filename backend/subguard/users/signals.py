from datetime import timedelta

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from users.models import UserVerfication


@receiver(signal=post_save, sender=UserVerfication)
def invalidate_previous_verification_links(sender: UserVerfication, instance: UserVerfication, created: bool, *args, **kawrgs) -> None:

    if not created:
        return
    
    UserVerfication.objects.filter(
        user=instance.user
    ).exclude(pk=instance.pk).update(
        expires_at=timezone.now() - timedelta(minutes=30)
    )