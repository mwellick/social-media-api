from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Post, Comment, Like
from api.serializers import PostListSerializer, PostRetrieveSerializer

POST_URL = reverse("social_media_api:post-list")


def detail_url(post_id):
    return reverse("social_media_api:post-detail", args=[post_id])


class UnauthenticatedPostApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(POST_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedPostApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="Test@test.test", password="Testpsw1", username="test_user"
        )
        self.user_2 = get_user_model().objects.create_user(
            email="Test@test2.test", password="Testpsw2", username="user2"
        )
        self.client.force_authenticate(self.user)

        self.post_1 = Post.objects.create(
            author=self.user,
            title="test_title",
            content="test content"
        )
        self.post_2 = Post.objects.create(
            author=self.user_2,
            title="test title_post 2",
            content="test content 2"
        )

    def test_post_list(self):
        res = self.client.get(POST_URL)
        posts = Post.objects.all()
        serializer = PostListSerializer(posts, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_filter_post_by_username(self):
        res = self.client.get(POST_URL, data={"username": "test_us"})
        serializer1 = PostListSerializer(self.post_1)
        serializer2 = PostListSerializer(self.post_2)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serializer1.data, res.data["results"])
        self.assertNotIn(serializer2.data, res.data["results"])

    def test_retrieve_post_detail(self):
        res = self.client.get(detail_url(self.post_1.id))
        serializer = PostRetrieveSerializer(self.post_1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_post(self):
        payload = {
            "author": self.user.id,
            "title": "updated title",
            "content": "updated content",
        }
        res = self.client.put(detail_url(self.post_1.id), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update_post_forbidden(self):
        payload = {"title": "updated title", "content": "updated content"}
        res = self.client.put(detail_url(self.post_2.id), payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_post(self):
        res = self.client.delete(detail_url(self.post_1.id))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_post_forbidden(self):
        res = self.client.delete(detail_url(self.post_2.id))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_comment(self):
        payload = {
            "comment_author": self.user.id,
            "post": self.post_2.id,
            "body": "test comment",
        }
        url = f"/api/social-media/posts/{self.post_2.id}/add-comment/"
        res = self.client.post(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_like_post(self):
        payload = {
            "user": self.user.id,
            "post": self.post_2.id,
        }
        url = f"/api/social-media/posts/{self.post_2.id}/like-post/"
        res = self.client.post(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), 1)

    def test_unlike_post(self):
        Like.objects.create(user=self.user, post=self.post_2)
        url = f"/api/social-media/posts/{self.post_2.id}/unlike-post/"
        res = self.client.post(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Like.objects.count(), 0)


class AdminPostTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="Test@admin.test",
            password="Testpsw1",
            username="test_admin",
            is_staff=True,
        )
        self.user_2 = get_user_model().objects.create_user(
            email="Test@test2.test", password="Testpsw2", username="user2"
        )
        self.client.force_authenticate(self.user)

        self.post_1 = Post.objects.create(
            author=self.user, title="test title", content="test content"
        )
        self.post_2 = Post.objects.create(
            author=self.user_2, title="test title 2", content="test content 2"
        )

    def test_admin_can_delete_any_post(self):
        res = self.client.delete(detail_url(self.post_2.id))
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_invalid_post(self):
        invalid_id = self.post_2.id + 1
        res = self.client.get(detail_url(invalid_id))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
