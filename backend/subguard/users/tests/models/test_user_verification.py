from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from django.test import TestCase
from django.utils import timezone as django_timezone
from users.models import User, UserVerfication


class UserVerificationModelTest(TestCase):

    def setUp(self) -> None:
        self.user: User = User.objects.create_user(email="test_user@mail.com", password="foo")
        self.user_verification: UserVerfication = UserVerfication.objects.create(user=self.user)

    def test_string_representation(self) -> None:
        self.assertEqual(
            str(self.user_verification),
            f"UserVerification(id='{self.user_verification.id}', email='{self.user_verification.user.email}')"
        )

    @patch("django.utils.timezone.now")
    def test_expires_at_sets_to_fifteen_minutes_from_now(self, mock_now) -> None:
        mock_now.return_value = datetime(2025, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        expected_expires_at = datetime(2025, 1, 1, 10, 15, 0, tzinfo=timezone.utc)
        user_verification: UserVerfication = UserVerfication.objects.create(user=self.user)
        self.assertEqual(user_verification.expires_at, expected_expires_at)

    def test_is_expired_should_return_false_for_non_expired_verifications(self) -> None:
        self.user_verification.expires_at = django_timezone.now() - timedelta(minutes=15)
        self.user_verification.save()
        self.assertTrue(self.user_verification.is_expired)

    def test_is_expired_should_return_true_for_expired_verifications(self) -> None:
        self.user_verification.expires_at = django_timezone.now() + timedelta(minutes=15)
        self.user_verification.save()
        self.assertFalse(self.user_verification.is_expired)

    @patch("django.core.mail.EmailMultiAlternatives.send")
    def test_send_verification_email_should_send_email(self, mock_send):
        self.user_verification.send_verification_email()
        mock_send.assert_called_once()
        