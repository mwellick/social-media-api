from rest_framework import serializers
from .models import (
    Post,
    Comment,
    Like,
    Follow,
    Unfollow
)


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "content",
            "published_date",
            "post_media"
        ]