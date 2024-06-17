from rest_framework.viewsets import ModelViewSet

from .models import (
    Post,
    Comment,
    Like,
    Follow,
    Unfollow
)

from .serializers import (
    PostSerializer,
    PostListSerializer,
    PostRetrieveSerializer,
    CommentSerializer,
    CommentListSerializer,
    CommentRetrieveSerializer,
    LikeSerializer,
    LikeListSerializer,
    LikeRetrieveSerializer,
    FollowSerializer,
    FollowListSerializer,
    FollowRetrieveSerializer,
    UnfollowSerializer,
    UnfollowListSerializer,
    UnfollowRetrieveSerializer
)


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class LikeViewSet(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class FollowViewSet(ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer


class UnfollowViewSet(ModelViewSet):
    queryset = Unfollow.objects.all()
    serializer_class = UnfollowSerializer
