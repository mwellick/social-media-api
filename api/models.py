import pathlib
import uuid

from django.db import models
from django.conf import settings
from django.utils.text import slugify

from user.models import User


def post_image_path(instance: "Post", filename: str) -> pathlib.Path:
    filename = (
        f"{slugify(instance.title)}-{uuid.uuid4()}" + pathlib.Path(filename).suffix
    )
    return pathlib.Path("upload/posts") / pathlib.Path(filename)


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    post_media = models.ImageField(blank=True, null=True, upload_to=post_image_path)

    def __str__(self):
        return f" {self.title}: {self.content[:20]}..."


class Comment(models.Model):
    comment_author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.comment_author} left a comment on a " f"{self.post.author} post"


class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="likes"
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_likes")
    is_liked = models.BooleanField(default=False)

    @staticmethod
    def unique_like(user: str, post: str, error_to_raise):
        if Like.objects.filter(user__username=user, post__content=post).exists():
            raise error_to_raise("You have already liked this post.")
        return {"user": user, "post": post}

    def clean(self):
        Like.unique_like(self.user.username, self.post.content, ValueError)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.full_clean()
        super(Like, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f"@{self.user.username} liked " f"@{self.post.author.username} post"


class Follow(models.Model):
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following"
    )
    followed_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followers"
    )
    followed_at = models.DateTimeField(auto_now_add=True)
    is_followed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.follower.username} followed {self.following.username}"

    @staticmethod
    def unique_follow(follower: str, followed: str, error_to_raise):
        if follower == followed:
            raise error_to_raise("You can't follow yourself")
        if Follow.objects.filter(
            follower__username=follower, followed_user__username=followed
        ).exists():
            raise error_to_raise("You have already followed this user.")
        return {"follower": follower, "followed": followed}

    def clean(self):
        Follow.unique_follow(
            self.follower.username, self.followed_user.username, ValueError
        )

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.full_clean()
        super(Follow, self).save(force_insert, force_update, using, update_fields)
