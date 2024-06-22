from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

class ManageUserProfile(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="Test@test.test",
            password="Testpsw1",
            username="test_user"
        )
        self.user_2 = get_user_model().objects.create_user(
            email="Test@test2.test",
            password="Testpsw2",
            username="user2"
        )
        self.client.force_authenticate(self.user)

    def test_logout_user(self):
        url = "/api/user/me/logout"
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(self.user.online)

    def test_delete_user_account(self):
        url = f"/api/user/me/"
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(get_user_model().objects.count(),1)
