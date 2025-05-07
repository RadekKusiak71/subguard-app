from django.http import HttpResponse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User


class ObtainTokenTests(APITestCase):


    def test_claiming_token_as_unverified_user_should_raise_401_with_code(self) -> None:
        user: User = User.objects.create_user(email="test_user@mail.com", password="foo", is_verified=False)
        response: HttpResponse = self.client.post("/api/token/", data={
            "email":user.email,
            "password": "foo"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual("not_verified", response.data.get("code"))
        self.assertIn("code", response.data)
        self.assertIn("detail", response.data)