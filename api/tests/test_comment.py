from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Post, Comment
from api.serializers import CommentListSerializer, CommentRetrieveSerializer

COMMENT_URL = reverse("social_media_api:comment-list")


def detail_url(comment_id):
    return reverse("social_media_api:comment-detail", args=[comment_id])


class UnauthenticatedCommentApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(COMMENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedCommentApiTests(TestCase):

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
            content="test content",
        )
        self.comment_1 = Comment.objects.create(
            comment_author=self.user, post=self.post_1, body="test comment"
        )
        self.comment_2 = Comment.objects.create(
            comment_author=self.user_2, post=self.post_1, body="test comment"
        )

    def test_comment_list(self):
        res = self.client.get(COMMENT_URL)
        comments = Comment.objects.all()
        serializer = CommentListSerializer(comments, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_filter_post_by_username(self):
        res = self.client.get(COMMENT_URL, data={"username": "test_us"})
        serializer1 = CommentListSerializer(self.comment_1)
        serializer2 = CommentListSerializer(self.comment_2)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serializer1.data, res.data["results"])
        self.assertNotIn(serializer2.data, res.data["results"])

    def test_retrieve_comment_detail(self):
        res = self.client.get(detail_url(self.comment_1.id))
        serializer = CommentRetrieveSerializer(self.comment_1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_comment(self):
        payload = {
            "body": "updated comment",
        }
        res = self.client.put(detail_url(self.comment_1.id), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update_comment_forbidden(self):
        payload = {
            "body": "updated comment",
        }
        res = self.client.put(detail_url(self.comment_2.id), payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_comment(self):
        res = self.client.delete(detail_url(self.comment_1.id))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_comment_forbidden(self):
        res = self.client.delete(detail_url(self.comment_2.id))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminCommentApiTests(TestCase):

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
            author=self.user,
            title="test_title",
            content="test content",
        )
        self.comment_1 = Comment.objects.create(
            comment_author=self.user, post=self.post_1, body="test comment"
        )
        self.comment_2 = Comment.objects.create(
            comment_author=self.user_2, post=self.post_1, body="test comment"
        )

    def test_admin_can_update_any_comment(self):
        payload = {
            "body": "updated comment",
        }
        res = self.client.put(detail_url(self.comment_2.id), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_admin_can_delete_any_comment(self):
        res = self.client.delete(detail_url(self.comment_2.id))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_invalid_comment(self):
        invalid_id = self.comment_2.id + 1
        res = self.client.get(detail_url(invalid_id))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
