from rest_framework import serializers
from users.models import User, UserVerfication


class UserVerificationSerializer(serializers.Serializer):

    def __init__(self, user_verification: UserVerfication, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.user_verification = user_verification

    def validate(self, attrs: dict) -> dict:
        if self.user_verification.is_expired:
            raise serializers.ValidationError({"detail": "User verification link is expired."})
        if self.user_verification.user.is_verified:
            raise serializers.ValidationError({"detail": "User if already verified."})
        return super().validate(attrs)

    def verify(self) -> None:
        user: User = self.user_verification.user
        user.is_verified = True
        user.save()


class ResendUserVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


    def resend(self) -> None:
        user: User | None = User.objects.filter(email=self.validated_data.get("email")).first()

        if not user:
            return
        
        if user.is_verified:
            return
        
        user_verification: UserVerfication = UserVerfication.objects.create(
            user=user
        )
        user_verification.send_verification_email()
