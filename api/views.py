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
        if self.action == "list":
            return PostListSerializer
        elif self.action == "retrieve":
            return PostRetrieveSerializer
        return PostListSerializer

    def get_queryset(self):
        queryset = self.queryset
        username = self.request.query_params.get("username")
        year = self.request.query_params.get("year")
        month = self.request.query_params.get("month")
        day = self.request.query_params.get("day")
        if username:
            queryset = queryset.filter(author__username__icontains=username)

        if year:
            queryset = queryset.filter(published_date__year=year)

        if month:
            queryset = queryset.filter(published_date__month=month)

        if day:
            queryset = queryset.filter(published_date__day=day)
        if self.action in ("list", "retrieve"):
            return queryset.select_related("author")
        return queryset


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = self.queryset
        username = self.request.query_params.get("username")
        year = self.request.query_params.get("year")
        month = self.request.query_params.get("month")
        day = self.request.query_params.get("day")
        if username:
            queryset = queryset.filter(comment_author__username__icontains=username)

        if year:
            queryset = queryset.filter(published_date__year=year)

        if month:
            queryset = queryset.filter(published_date__month=month)

        if day:
            queryset = queryset.filter(published_date__day=day)

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
        username = self.request.query_params.get("username")
        if username:
            queryset = queryset.filter(user__username__icontains=username)
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
        follower = self.request.query_params.get("follower")
        followed_user = self.request.query_params.get("followed")
        if follower:
            queryset = queryset.filter(follower__username__icontains=follower)
        if followed_user:
            queryset = queryset.filter(followed_user__username__icontains=followed_user)
        if self.action in ("list", "retrieve"):
            return queryset.select_related("follower", "followed_user")
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
        unfollower = self.request.query_params.get("unfollower")
        unfollowed_user = self.request.query_params.get("unfollowed")

        if unfollower:
            queryset = queryset.filter(unfollower__username__icontains=unfollower)
        if unfollowed_user:
            queryset = queryset.filter(unfollowed__username__icontains=unfollowed_user)
        if self.action in ("list", "retrieve"):
            return queryset.select_related("unfollower", "unfollowed_user")
        return queryset
