from django.http import HttpResponse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User


class UserRegisterTest(APITestCase):

    def setUp(self) -> None:
        self.register_path: str = '/api/users/register/'

    def test_post_register_with_valid_data_returns_201(self) -> None:
        response: HttpResponse = self.client.post(
            path=self.register_path,
            data={"email": "test_user@mail.com", "password": "!QAZ2wsx!@#", "password_confirmation": "!QAZ2wsx!@#"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_register_with_valid_data_creates_user_with_provided_data(self) -> None:
        response: HttpResponse = self.client.post(
            path=self.register_path,
            data={"email": "test_user@mail.com", "password": "!QAZ2wsx!@#", "password_confirmation": "!QAZ2wsx!@#"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="test_user@mail.com").exists())

    def test_post_register_with_not_unique_email_returns_400(self) -> None:
        User.objects.create_user(email="test_user@mail.com", password="!QAZ2wsx!@#")
        response: HttpResponse = self.client.post(
            path=self.register_path,
            data={"email": "test_user@mail.com", "password": "!QAZ2wsx!@#", "password_confirmation": "!QAZ2wsx!@#"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_register_with_invalid_email_format_returns_400(self) -> None:
        response: HttpResponse = self.client.post(
            path=self.register_path,
            data={"email": "test_usermail.com", "password": "!QAZ2wsx!@#", "password_confirmation": "!QAZ2wsx!@#"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_register_with_empty_email_returns_400(self) -> None:
        response: HttpResponse = self.client.post(
            path=self.register_path,
            data={"email": "", "password": "!QAZ2wsx!@#", "password_confirmation": "!QAZ2wsx!@#"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_register_without_email_returns_400(self) -> None:
        response: HttpResponse = self.client.post(
            path=self.register_path,
            data={"password": "!QAZ2wsx!@#", "password_confirmation": "!QAZ2wsx!@#"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_register_without_password_returns_400(self) -> None:
        response: HttpResponse = self.client.post(
            path=self.register_path,
            data={"email": "test_usermail.com", "password_confirmation": "!QAZ2wsx!@#"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_register_without_password_confirmation_returns_400(self) -> None:
        response: HttpResponse = self.client.post(
            path=self.register_path,
            data={"email": "test_usermail.com", "password": "!QAZ2wsx!@#",}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_register_with_non_matching_password_and_password_confirmation_returns_400(self) -> None:
        response: HttpResponse = self.client.post(
            path=self.register_path,
            data={"email": "test_usermail.com", "password": "!QAZ2wsx!@#", "password_confirmation": "!QAZ2wsx!@#NonMatching"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
