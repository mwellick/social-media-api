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
    author = serializers.CharField(source="author.email", read_only=True)

    class Meta:
        model = Post
        fields = ["id", "author", "published_date", "post_media"]


class PostRetrieveSerializer(PostListSerializer):
    class Meta(PostListSerializer.Meta):
        pass


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "comment_author", "post", "body", "created_at"]


class CommentListSerializer(serializers.ModelSerializer):
    comment_author = serializers.CharField(
        source="comment_author.email", read_only=True
    )
    post = serializers.CharField(
        source="post.author.email", read_only=True
    )

    class Meta:
        model = Comment
        exclude = ["body"]


class CommentRetrieveSerializer(serializers.ModelSerializer):
    comment_author = serializers.CharField(
        source="comment_author.email", read_only=True
    )
    post = serializers.CharField(
        source="post.author.email", read_only=True
    )

    class Meta:
        model = Comment
        fields = ["id", "comment_author", "post"]


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["id", "user", "post"]

    def validate(self, attrs):
        Like.unique_like(
            attrs["user"].username,
            attrs["post"].content,
            serializers.ValidationError
        )
        return attrs


class LikeListSerializer(LikeSerializer):
    user = serializers.CharField(
        source="user.email", read_only=True
    )
    post = serializers.CharField(
        source="post.author.email", read_only=True
    )

    class Meta:
        model = Like
        fields = [
            "id",
            "user",
            "post"
        ]


class LikeRetrieveSerializer(LikeListSerializer):
    class Meta:
        model = Like
        exclude = ["id"]


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = [
            "id",
            "follower",
            "following",
            "followed_at"
        ]

    def validate(self, attrs):
        Follow.unique_follow(
            attrs["follower"].username,
            attrs["following"].username,
            serializers.ValidationError
        )
        return attrs


class FollowListSerializer(serializers.ModelSerializer):
    follower = serializers.CharField(
        source="follower.email", read_only=True
    )
    following = serializers.CharField(
        source="following.email", read_only=True
    )

    class Meta:
        model = Follow
        fields = [
            "id",
            "follower",
            "following"
        ]


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
            "unfollowed",
        ]

    def validate(self, attrs):
        Unfollow.unique_unfollow(
            attrs["unfollower"].username,
            attrs["unfollowed"].username,
            serializers.ValidationError
        )
        return attrs


class UnfollowListSerializer(serializers.ModelSerializer):
    unfollower = serializers.CharField(
        source="unfollower.email", read_only=True
    )
    unfollowed = serializers.CharField(
        source="unfollowed.email", read_only=True
    )

    class Meta:
        model = Unfollow
        fields = [
            "id",
            "unfollower",
            "unfollowed",
        ]


class UnfollowRetrieveSerializer(UnfollowListSerializer):
    class Meta:
        model = Unfollow
        exclude = ["id"]
