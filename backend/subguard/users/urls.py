from typing import List
from django.urls import URLPattern, path
from users.views import UserRegisterCreateAPIView
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)


app_name = "users"

urlpatterns: List[URLPattern] = [
    path('users/register/', UserRegisterCreateAPIView.as_view(), name='user-register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]