from rest_framework import serializers
from .models import Post, Comment, Like, Follow, Unfollow


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "content",
            "published_date",
        ]


class PostListSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Post
        fields = ["id", "author", "published_date"]


class PostRetrieveSerializer(PostListSerializer):
    class Meta:
        model = Post
        exclude = ["id"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "comment_author", "post", "body", "created_at"]


class CommentListSerializer(serializers.ModelSerializer):
    comment_author = serializers.CharField(
        source="comment_author.username", read_only=True
    )
    commented_post = serializers.CharField(
        source="post.content", read_only=True
    )

    class Meta:
        model = Comment
        exclude = ["body", "post"]


class CommentRetrieveSerializer(serializers.ModelSerializer):
    comment_author = serializers.CharField(source="comment_author.username", read_only=True)
    commented_post = serializers.CharField(source="post.content", read_only=True)

    class Meta:
        model = Comment
        fields = ["comment_author", "body", "created_at", "commented_post"]


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["id", "user", "post"]

    def validate(self, attrs):
        Like.unique_like(
            attrs["user"].username, attrs["post"].content, serializers.ValidationError
        )
        return attrs


class LikeListSerializer(LikeSerializer):
    user_liked = serializers.CharField(source="user.username", read_only=True)
    liked_post = serializers.CharField(source="post.content", read_only=True)

    class Meta:
        model = Like
        fields = ["id", "user_liked", "liked_post"]


class LikeRetrieveSerializer(LikeListSerializer):
    posts_author = serializers.CharField(source="post.author.username", read_only=True)

    class Meta:
        model = Like
        fields = ["user_liked", "liked_post", "posts_author"]


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ["id", "follower", "followed_user", "followed_at"]

    def validate(self, attrs):
        Follow.unique_follow(
            attrs["follower"].username,
            attrs["followed_user"].username,
            serializers.ValidationError,
        )
        return attrs


class FollowListSerializer(serializers.ModelSerializer):
    follower = serializers.CharField(source="follower.username", read_only=True)
    followed_user = serializers.CharField(source="followed_user.username", read_only=True)

    class Meta:
        model = Follow
        fields = ["id", "follower", "followed_user"]


class FollowRetrieveSerializer(FollowListSerializer):
    class Meta:
        model = Follow
        exclude = ["id"]


class UnfollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unfollow
        fields = [
            "id",
            "unfollower",
            "unfollowed_user",
        ]

    def validate(self, attrs):
        Unfollow.unique_unfollow(
            attrs["unfollower"].username,
            attrs["unfollowed_user"].username,
            serializers.ValidationError,
        )
        return attrs


class UnfollowListSerializer(serializers.ModelSerializer):
    unfollower = serializers.CharField(source="unfollower.username", read_only=True)
    unfollowed = serializers.CharField(source="unfollowed_user.username", read_only=True)

    class Meta:
        model = Unfollow
        fields = [
            "id",
            "unfollower",
            "unfollowed_user",
        ]


class UnfollowRetrieveSerializer(UnfollowListSerializer):
    class Meta:
        model = Unfollow
        exclude = ["id"]
