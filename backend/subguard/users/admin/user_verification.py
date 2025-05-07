from django.contrib import admin
from users.models import UserVerfication


@admin.register(UserVerfication)
class UserVerificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user__email", "created_at", "is_expired")