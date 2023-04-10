from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse

from rest_framework import status

from rest_framework.test import APITestCase

from .models import Wallet
from django.contrib.auth.models import User


class WalletTest(APITestCase):
    def setUp(self):
        User.objects.create(username="admin", password="qwerty512228")
        User.objects.create(username="mmas", password="qwerty512228")

        Wallet.objects.create(
            name="AAQQPD8Z",
            type_of_wallet="VISA",
            currency="USD",
            owner=User.objects.get(username="admin"),
        )

    @property
    def bearer_token(self):
        user = User.objects.get(username="admin")
        refresh = RefreshToken.for_user(user)
        return {"HTTP_AUTHORIZATION": f"Bearer {refresh.access_token}"}

    def test_get_list_wallet(self):
        url = reverse("wallet_list")
        response = self.client.get(url, **self.bearer_token)
        response1 = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(len(response1.data), 0)

    def test_post_create_wallet(self):
        url = reverse("wallet_create")
        data = {
            "type_of_wallet": "VISA",
            "currency": "USD",
        }
        response = self.client.post(url, data, format="json", **self.bearer_token)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Wallet.objects.count(), 2)

    def test_post_delete_wallet(self):
        url = reverse("wallet_detail_delete", args=["AAQQPD8Z"])
        response1 = self.client.delete(url)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(Wallet.objects.count(), 1)
        response = self.client.delete(url, **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Wallet.objects.count(), 0)

    def test_get_detail_wallet(self):
        url = reverse("wallet_detail_delete", args=["AAQQPD8Z"])
        response = self.client.get(url, **self.bearer_token)
        self.assertEqual(
            response.data["id"],
            1,
        )
        self.assertEqual(response.data["name"], "AAQQPD8Z")
        self.assertEqual(response.data["type_of_wallet"], "VISA")
        self.assertEqual(response.data["currency"], "USD")
        self.assertEqual(response.data["balance"], "3.00")
        self.assertEqual(response.data["owner"], 13)
