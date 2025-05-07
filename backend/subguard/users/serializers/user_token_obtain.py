from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from users.models import User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs: dict) -> dict:
        attrs: dict = super().validate(attrs)
        try:
            if not User.objects.get(email=self.initial_data.get("email")).is_verified:
                raise AuthenticationFailed(detail={"detail":"User is not verified.", "code": "not_verified"}, code="not_verified")
        except User.DoesNotExist:
            raise AuthenticationFailed()
        return attrs