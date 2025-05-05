from django.test import TestCase
from users.models import User
from django.db import IntegrityError


class UserModelTest(TestCase):

    def test_string_representation(self) -> None:
        user: User = User.objects.create_user(
            email="test_user@mail.com",
            password="foo"
        )
        self.assertEqual(
            str(user),
            f"User(id='{user.id}', email='{user.email}')"
        )

    def test_creating_user_with_taken_email_should_raise_error(self) -> None:
        User.objects.create_user(
            email="test_user@mail.com",
            password="foo"
        )

        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email="test_user@mail.com",
                password="foo"
            )

