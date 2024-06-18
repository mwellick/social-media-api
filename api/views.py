from rest_framework.viewsets import ModelViewSet

from .models import Post, Comment, Like, Follow, Unfollow

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
    UnfollowRetrieveSerializer,
)


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return PostListSerializer
        return PostListSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action in ("list", "retrieve"):
            return queryset.select_related("author")
        return queryset


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action in ("list", "retrieve"):
            return queryset.select_related("comment_author", "post")
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return CommentListSerializer
        elif self.action == "retrieve":
            return CommentRetrieveSerializer
        return CommentSerializer


class LikeViewSet(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return LikeListSerializer
        elif self.action == "retrieve":
            return LikeRetrieveSerializer
        return LikeSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action in ("list", "retrieve"):
            return queryset.select_related("user", "post")
        return queryset


class FollowViewSet(ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return FollowListSerializer
        elif self.action == "retrieve":
            return FollowRetrieveSerializer
        return FollowSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action in ("list", "retrieve"):
            return queryset.select_related("follower", "following")
        return queryset


class UnfollowViewSet(ModelViewSet):
    queryset = Unfollow.objects.all()
    serializer_class = UnfollowSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return UnfollowListSerializer
        elif self.action == "retrieve":
            return UnfollowRetrieveSerializer
        return UnfollowSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action in ("list", "retrieve"):
            return queryset.select_related("unfollower", "unfollowed")
        return queryset
