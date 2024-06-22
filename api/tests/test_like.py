from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Post, Comment, Like
from api.serializers import CommentListSerializer, CommentRetrieveSerializer, LikeListSerializer, LikeRetrieveSerializer

LIKE_URL = reverse("social_media_api:like-list")


def detail_url(like_id):
    return reverse("social_media_api:like-detail", args=[like_id])


class UnauthenticatedLikeApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(LIKE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedLikeApiTests(TestCase):

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

        self.post_1 = Post.objects.create(
            author=self.user,
            title="test_title",
            content="test content",
        )
        self.comment_1 = Comment.objects.create(
            comment_author=self.user,
            post=self.post_1,
            body="test comment"

        )
        self.comment_2 = Comment.objects.create(
            comment_author=self.user_2,
            post=self.post_1,
            body="test comment"
        )
        self.like_1 = Like.objects.create(
            user=self.user,
            post=self.post_1
        )
        self.like_2 = Like.objects.create(
            user=self.user_2,
            post=self.post_1
        )

    def test_like_list(self):
        res = self.client.get(LIKE_URL)
        likes = Like.objects.all()
        serializer = LikeListSerializer(likes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)
        self.assertEqual(Like.objects.count(), 2)

    def test_filter_likes_by_username(self):
        res = self.client.get(LIKE_URL, data={"username": "test_us"})
        serializer1 = LikeListSerializer(self.like_1)
        serializer2 = LikeListSerializer(self.like_2)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serializer1.data, res.data["results"])
        self.assertNotIn(serializer2.data, res.data["results"])

    def test_retrieve_like_detail(self):
        res = self.client.get(detail_url(self.like_1.id))
        serializer = LikeRetrieveSerializer(self.like_1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_delete_like_from_history_forbidden(self):
        res = self.client.delete(detail_url(self.like_2.id))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
