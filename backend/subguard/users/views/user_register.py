from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from users.serializers import UserRegisterSerializer


class UserRegisterCreateAPIView(CreateAPIView):
    serializer_class = UserRegisterSerializer

    @extend_schema(
        tags=["Users"],
        summary="User Registration",
        responses={
            status.HTTP_201_CREATED: UserRegisterSerializer,
            status.HTTP_400_BAD_REQUEST: None,
        },
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Register a new user account.

        This endpoint allows new users to create an account by providing the required credentials.  
        """
        return super().post(request, *args, **kwargs)