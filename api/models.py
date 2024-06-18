from django.db import models
from django.conf import settings
from user.models import User


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
    )
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    post_media = models.ImageField(blank=True, null=True)

    def __str__(self):
        return f" {self.author}: {self.content[:20]}..."


class Comment(models.Model):
    comment_author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.comment_author} left a comment on a "
            f"{self.post_comment.author} post"
        )


class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="likes"
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_likes")

    def __str__(self):
        return (
            f"@{self.user.username} liked " f"@{self.liked_post.author.username} post"
        )


class Follow(models.Model):
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following"
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followers"
    )
    followed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower.username} followed {self.following.username}"


class Unfollow(models.Model):
    unfollower = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="unfollowing"
    )
    unfollowed = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="unfollowers"
    )
    unfollowed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.unfollower.username} unfollowed {self.unfollower.username}"
