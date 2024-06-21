from rest_framework import serializers
from .models import Post, Comment, Like, Follow


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "title",
            "content",
            "published_date",
            "post_media"
        ]


class PostListSerializer(serializers.ModelSerializer):
    author = serializers.CharField(
        source="author.username",
        read_only=True
    )
    likes = serializers.IntegerField(
        source="post_likes.count",
        read_only=True
    )
    comments = serializers.IntegerField(
        source="comments.count",
        read_only=True
    )

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "author",
            "comments",
            "likes",
            "published_date"
        ]


class PostRetrieveSerializer(PostListSerializer):
    class Meta:
        model = Post
        fields = [
            "title",
            "author",
            "likes",
            "published_date"
        ]


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "comment_author",
            "post",
            "body"
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["comment_author"] = request.user
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "comment_author",
            "post",
            "body",
            "created_at"
        ]


class CommentListSerializer(serializers.ModelSerializer):
    comment_author = serializers.CharField(
        source="comment_author.username",
        read_only=True
    )
    commented_post = serializers.CharField(
        source="post.content",
        read_only=True
    )

    class Meta:
        model = Comment
        exclude = ["body", "post"]


class CommentRetrieveSerializer(serializers.ModelSerializer):
    comment_author = serializers.CharField(
        source="comment_author.username",
        read_only=True
    )
    commented_post = serializers.CharField(
        source="post.content",
        read_only=True
    )

    class Meta:
        model = Comment
        fields = [
            "comment_author",
            "body",
            "created_at",
            "commented_post"
        ]


class CreateLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["user", "post"]

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["user"] = request.user
        return super().create(validated_data)

    def validate(self, attrs):
        Like.unique_like(
            attrs["user"].username, attrs["post"].content, serializers.ValidationError
        )
        return attrs


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["id", "user", "post"]


class LikeListSerializer(LikeSerializer):
    user_liked = serializers.CharField(
        source="user.username",
        read_only=True
    )
    liked_post = serializers.CharField(
        source="post.content",
        read_only=True
    )

    class Meta:
        model = Like
        fields = [
            "id",
            "user_liked",
            "liked_post"
        ]


class LikeRetrieveSerializer(LikeListSerializer):
    posts_author = serializers.CharField(source="post.author.username", read_only=True)

    class Meta:
        model = Like
        fields = [
            "user_liked",
            "liked_post",
            "posts_author"
        ]


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = [
            "id",
            "follower",
            "followed_user",
            "followed_at"
        ]

    def validate(self, attrs):
        Follow.unique_follow(
            attrs["follower"].username,
            attrs["followed_user"].username,
            serializers.ValidationError,
        )
        return attrs


class FollowListSerializer(serializers.ModelSerializer):
    follower = serializers.CharField(
        source="follower.username",
        read_only=True
    )
    followed_user = serializers.CharField(
        source="followed_user.username",
        read_only=True
    )

    class Meta:
        model = Follow
        fields = [
            "id",
            "follower",
            "followed_user"
        ]


class FollowRetrieveSerializer(FollowListSerializer):
    class Meta:
        model = Follow
        exclude = ["id", "is_followed"]
