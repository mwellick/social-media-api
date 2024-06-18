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
    class Meta:
        model = Post
        fields = ["id", "author", "content", "published_date", "post_media"]


class PostRetrieveSerializer(PostListSerializer):
    class Meta(PostListSerializer.Meta):
        pass


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "comment_author", "post_comment", "body", "created_at"]


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ["id"]


class CommentRetrieveSerializer(CommentListSerializer):
    class Meta(CommentListSerializer.Meta):
        pass


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["id", "user", "post"]


class LikeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        exclude = ["id"]


class LikeRetrieveSerializer(LikeListSerializer):
    class Meta(LikeListSerializer.Meta):
        pass


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ["id", "follower", "following", "followed_at"]


class FollowListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        exclude = ["id", "followed_at"]


class FollowRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ["followed_at"]


class UnfollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unfollow
        fields = [
            "id",
            "unfollower",
            "unfollowed",
        ]


class UnfollowListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unfollow
        exclude = ["id", "unfollowed_at"]


class UnfollowRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unfollow
        fields = ["unfollowed_at"]
