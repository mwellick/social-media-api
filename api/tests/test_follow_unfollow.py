from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Follow
from api.serializers import FollowListSerializer, FollowRetrieveSerializer

FOLLOW_URL = reverse("social_media_api:follow-list")


def detail_url(follow_id):
    return reverse("social_media_api:follow-detail", args=[follow_id])


class UnauthenticatedFollowApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(FOLLOW_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedFollowApiTests(TestCase):

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
        self.follow = Follow.objects.create(
            follower=self.user,
            followed_user=self.user_2
        )
        self.follow_2 = Follow.objects.create(
            follower=self.user_2,
            followed_user=self.user
        )

    def test_follow_list(self):
        res = self.client.get(FOLLOW_URL)
        follows = Follow.objects.all()
        serializer = FollowListSerializer(follows, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)
        self.assertEqual(Follow.objects.count(), 2)

    def test_filter_follow_by_follower_username(self):
        res = self.client.get(FOLLOW_URL, data={"follower": "test_us"})
        serializer1 = FollowListSerializer(self.follow)
        serializer2 = FollowListSerializer(self.follow_2)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serializer1.data, res.data["results"])
        self.assertNotIn(serializer2.data, res.data["results"])

    def test_filter_follow_by_followed_username(self):
        res = self.client.get(FOLLOW_URL, data={"followed": "test_us"})
        serializer1 = FollowListSerializer(self.follow)
        serializer2 = FollowListSerializer(self.follow_2)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serializer2.data, res.data["results"])
        self.assertNotIn(serializer1.data, res.data["results"])

    def test_retrieve_follow_detail(self):
        res = self.client.get(detail_url(self.follow.id))
        serializer = FollowRetrieveSerializer(self.follow)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_delete_follow_from_history_forbidden(self):
        res = self.client.delete(detail_url(self.follow.id))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_follow_user(self):
        self.user_3 = get_user_model().objects.create_user(
            email="Test@test.test3",
            password="Testpsw3",
            username="test_user3"
        )
        self.client.force_authenticate(self.user_3)
        url = f"/api/user/{self.user_2.username}/follow/"
        res = self.client.post(url)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_unfollow_user(self):
        self.client.force_authenticate(self.user_2)
        url = f"/api/user/{self.user.username}/unfollow/"
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
