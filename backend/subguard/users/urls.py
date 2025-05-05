from typing import List
from django.urls import URLPattern, path
from users.views import UserRegisterCreateAPIView

app_name = "users"

urlpatterns: List[URLPattern] = [
    path('users/register/', UserRegisterCreateAPIView.as_view(), name='user-register'),
]