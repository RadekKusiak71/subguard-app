from django.db.models import QuerySet
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import UserVerfication
from users.serializers import (ResendUserVerificationSerializer,
                               UserVerificationSerializer)


class VerifyUserAccountAPIView(APIView):

    def get_queryset(self) -> QuerySet[UserVerfication]:
        if hasattr(self, "swagger_fake_view"):
            return UserVerfication.objects.none()
        return UserVerfication.objects.all()

    def get(self, request: Request, *args, **kwargs) -> Response:
        verification: UserVerfication = get_object_or_404(self.get_queryset(), pk=kwargs.get("verification_id"))
        serializer: UserVerificationSerializer = UserVerificationSerializer(data={}, user_verification=verification)
        serializer.is_valid(raise_exception=True)
        serializer.verify()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ResendUserVerificationAPIView(APIView):
    
    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer: ResendUserVerificationSerializer = ResendUserVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.resend()
        return Response(status=status.HTTP_201_CREATED)