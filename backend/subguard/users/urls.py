from typing import List

from django.urls import URLPattern, path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)
from users.views import (ResendUserVerificationAPIView,
                         UserRegisterCreateAPIView, VerifyUserAccountAPIView)

app_name = "users"

urlpatterns: List[URLPattern] = [
    path('users/register/', UserRegisterCreateAPIView.as_view(), name='user-register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verification/<str:verification_id>/confirm/', VerifyUserAccountAPIView.as_view(), name='verify-user-account'),
    path('verification/resend/', ResendUserVerificationAPIView.as_view(), name='resend-user-verifictaion'),
]