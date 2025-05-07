from datetime import timedelta
from unittest.mock import patch

from django.http import HttpResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User, UserVerfication


class ResendUserVerificationCodeTests(APITestCase):

    def setUp(self) -> None:
        self.verify_account_path: str = "/api/verification"
        self.user: User = User.objects.create_user(email="test_user@mail.com", password="foo")
        self.user_verification: UserVerfication = UserVerfication.objects.create(user=self.user)

    @staticmethod
    def get_verification_link(verification_id: str) -> str:
        return f"verification/{verification_id}/confirm/"

    def test_verify_user_with_valid_verification_id_should_change_user_is_verified_status(self) -> None:
        response: HttpResponse = self.client.get(path=ResendUserVerificationCodeTests.get_verification_link(self.user_verification.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_verified)

    def test_verify_user_with_invalid_verification_id_returns_404(self) -> None:
        response: HttpResponse = self.client.get(path=ResendUserVerificationCodeTests.get_verification_link("INVALID_ID"))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_verify_already_verified_user_returns_400(self) -> None:
        response: HttpResponse = self.client.get(path=ResendUserVerificationCodeTests.get_verification_link(self.user_verification.id))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)

    def test_verify_user_with_expired_verification_id_returns_400(self) -> None:
        self.user_verification.expires_at = timezone.now() - timedelta(minutes=15)
        self.user_verification.save()
        response: HttpResponse = self.client.get(path=ResendUserVerificationCodeTests.get_verification_link(self.user_verification.id))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)
