from unittest.mock import patch

from django.http import HttpResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User, UserVerfication


class ResendUserVerificationCodeTests(APITestCase):

    def setUp(self) -> None:
        self.resend_account_verification_path: str = "/api/verification/resend/"
        self.user: User = User.objects.create_user(email="test_user@mail.com", password="foo")
        self.user_verification: UserVerfication = UserVerfication.objects.create(user=self.user)

    @patch("django.core.mail.EmailMultiAlternatives.send")
    def test_resend_verification_with_valid_email_sends_email(self, mock_send):
        response: HttpResponse = self.client.post(
            path=self.resend_account_verification_path,
            data={"email": self.user.email}
        )
        self.user_verification.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(self.user_verification.is_expired)
        self.assertTrue(UserVerfication.objects.filter(user__email="test_user@mail.com", expires_at__gt=timezone.now()))
        mock_send.assert_called_once()

    @patch("django.core.mail.EmailMultiAlternatives.send")
    def test_resend_verification_with_invalid_email_silent_fail(self, mock_send):
        response: HttpResponse = self.client.post(
            path=self.resend_account_verification_path,
            data={"email": "invalid_email@mail.com"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mock_send.assert_not_called()

    @patch("django.core.mail.EmailMultiAlternatives.send")
    def test_resend_verification_for_verified_user_silent_fail(self, mock_send):
        self.user.is_verified = True
        self.user.save()

        response: HttpResponse = self.client.post(
            path=self.resend_account_verification_path,
            data={"email": self.user.email}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mock_send.assert_not_called()
