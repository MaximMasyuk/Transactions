from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

from django.contrib.auth.models import User
from django.urls import reverse

from wallets.models import Wallet

from .models import Transaction


class TransactionTest(APITestCase):
    """Test class for Transaction"""

    def setUp(self) -> None:
        """Create the data for test database"""
        User.objects.create(username="admin", password="qwerty512228")
        User.objects.create(username="mmas", password="qwerty512228")

        Wallet.objects.create(
            id=1,
            name="AAQQPD8Z",
            type_of_wallet="VISA",
            currency="RUB",
            owner=User.objects.get(username="admin"),
        )

        Wallet.objects.create(
            id=2,
            name="QWER45QW",
            type_of_wallet="VISA",
            currency="RUB",
            owner=User.objects.get(username="admin"),
        )

        Wallet.objects.create(
            id=3,
            name="AQWS12QS",
            type_of_wallet="VISA",
            currency="USD",
            owner=User.objects.get(username="admin"),
        )

        Wallet.objects.create(
            id=4,
            name="CVBN67IK",
            type_of_wallet="VISA",
            currency="RUB",
            owner=User.objects.get(username="mmas"),
        )

        Transaction.objects.create(
            id=5,
            sender=Wallet.objects.get(pk=1),
            receiver=Wallet.objects.get(pk=2),
            transfer_amount=10.00,
            commission=0.00,
            status="PAID",
        )

    @property
    def bearer_token(self):
        """Create the token for user"""
        user = User.objects.get(username="admin")
        refresh = RefreshToken.for_user(user)
        return {"HTTP_AUTHORIZATION": f"Bearer {refresh.access_token}"}

    def test_get_list_transaction(self):
        """Test the view transaction_list"""
        url = reverse("transactions_list")
        response = self.client.get(url, **self.bearer_token)
        response1 = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response1.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_list_for_name_transaction(self):
        """Test the view transaction_list_for_name"""
        url = reverse("transaction_list_for_name", args=["AAQQPD8Z"])
        url1 = reverse("transaction_list_for_name", args=["RFED12ED"])
        response = self.client.get(url, **self.bearer_token)
        response1 = self.client.get(url1, **self.bearer_token)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response1.data, {"error": "transaction does not exist"})

    def test_get_delete_transaction(self):
        """Test the view transaction_detail_delete"""
        url = reverse("transactions_detail_delete", args=["5"])
        url1 = reverse("transactions_detail_delete", args=["7"])

        response = self.client.delete(url, **self.bearer_token)
        response1 = self.client.delete(url1, **self.bearer_token)
        response2 = self.client.delete(url)
        self.assertEqual(response.data, {"Status": "transaction was delete"})
        self.assertEqual(response1.data, {"error": "transaction does not exist"})
        self.assertEqual(response2.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_detail_transaction(self):
        """Test the view transaction_detail_delete"""
        url = reverse("transactions_detail_delete", args=[5])
        response = self.client.get(url, **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["id"],
            5,  # Update to the actual value returned in the response
        )

        self.assertEqual(
            response.data["sender"],
            1,
        )
        self.assertEqual(
            response.data["receiver"],
            2,
        )
        self.assertEqual(
            response.data["transfer_amount"],
            "10.00",
        )
        self.assertEqual(
            response.data["commission"],
            "0.00",
        )
        self.assertEqual(
            response.data["status"],
            "PAID",
        )
        self.assertIn(
            "timestamp",
            response.data,
        )

    def test_post_create_transaction(self):
        """test the view transaction_create"""
        url = reverse("transaction_create")
        data = {"sender": 1, "receiver": 2, "transfer_amount": 10.0}

        response = self.client.post(url, data=data, format="json", **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Transaction.objects.count(), 2)
