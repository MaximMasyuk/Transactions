from rest_framework.test import APITestCase

from rest_framework import status


from django.contrib.auth.models import User
from django.urls import reverse


class UserTest(APITestCase):
    """Test class for Transaction"""

    def setUp(self):
        """Create the data for test database"""
        User.objects.create(username="admin", password="qwerty512228")

    def test__post_register_user(self):
        """test the view TokenObtainPairView"""
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
