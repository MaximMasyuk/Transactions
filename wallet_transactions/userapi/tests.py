from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status


from django.contrib.auth.models import User
from django.urls import reverse


class UserTest(APITestCase):
    def setUp(self):
        User.objects.create(username="admin", password="qwerty512228")

    @property
    def bearer_token(self):
        user = User.objects.get(username="admin")
        refresh = RefreshToken.for_user(user)
        return {"HTTP_AUTHORIZATION": f"Bearer {refresh.access_token}"}

    def test__post_register_user(self):
        url = reverse("token_register")
        data = {
            "username": "mmmas",
            "password": "qwerty123",
            "first_name": "max",
            "last_name": "mmas",
        }
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 2)
