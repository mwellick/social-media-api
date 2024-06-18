from django.db import models
from django.conf import settings
from django.db.models import UniqueConstraint

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
            f"{self.post.author} post"
        )


class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="likes"
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="post_likes"
    )

    @staticmethod
    def unique_like(user: str, post: str, error_to_raise):
        if Like.objects.filter(
                user__username=user,
                post__content=post
        ).exists():
            raise error_to_raise("You have already liked this post.")
        return {"user": user, "post": post}

    def clean(self):
        Like.unique_like(
            self.user.username,
            self.post.content,
            ValueError
        )

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None
    ):
        self.full_clean()
        super(Like, self).save(
            force_insert,
            force_update,
            using,
            update_fields
        )

    def __str__(self):
        return (
            f"@{self.user.username} liked " f"@{self.post.author.username} post"
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

    @staticmethod
    def unique_follow(follower: str, following: str, error_to_raise):
        if follower == following:
            raise error_to_raise("You can't follow yourself")
        if Follow.objects.filter(
                follower__username=follower,
                following__username=following
        ).exists():
            raise error_to_raise("You have already followed this user.")
        return {"follower": follower, "following": following}

    def clean(self):
        Follow.unique_follow(
            self.follower.username,
            self.following.username,
            ValueError
        )

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None
    ):
        self.full_clean()
        super(Follow, self).save(
            force_insert,
            force_update,
            using,
            update_fields
        )


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

    @staticmethod
    def unique_unfollow(unfollower: str, unfollowed: str, error_to_raise):
        if unfollower == unfollowed:
            raise error_to_raise("This action cannot be realized")
        if Unfollow.objects.filter(
                unfollower__username=unfollower,
                unfollowed__username=unfollowed
        ).exists():
            raise error_to_raise("You have already unfollowed this user.")
        return {"unfollower": unfollower, "unfollowed": unfollowed}

    def clean(self):
        Unfollow.unique_unfollow(
            self.unfollower.username,
            self.unfollowed.username,
            ValueError
        )

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None
    ):
        self.full_clean()
        super(Unfollow, self).save(
            force_insert,
            force_update,
            using,
            update_fields
        )
