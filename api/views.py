from django.contrib.auth import get_user_model
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
)
from rest_framework import status, generics, mixins
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Post, Comment, Like, Follow

from .serializers import (
    PostSerializer,
    PostListSerializer,
    PostRetrieveSerializer,
    CommentSerializer,
    CommentListSerializer,
    CommentRetrieveSerializer,
    CreateCommentSerializer,
    LikeSerializer,
    LikeListSerializer,
    LikeRetrieveSerializer,
    FollowSerializer,
    FollowListSerializer,
    FollowRetrieveSerializer,
    CreateLikeSerializer,
)


@extend_schema_view(
    create=extend_schema(summary="Create a post", description="User can create a post"),
    retrieve=extend_schema(
        summary="Get a detailed info about specific post",
        description="User can get a detailed info about own post",
    ),
    update=extend_schema(
        summary="Update info about specific post",
        description="User can update information about own post or admin can update any",
    ),
    partial_update=extend_schema(
        summary="Partial update of specific post",
        description="User can make a partial update of own post or admin can update any",
    ),
    destroy=extend_schema(
        summary="Delete a post",
        description="User can delete own post or admin can delete any post",
    ),
)
class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_serializer_class(self):
        if self.action in ("like_post", "unlike_post"):
            return CreateLikeSerializer
        if self.action == "add_comment":
            return CreateCommentSerializer
        if self.action == "list":
            return PostListSerializer
        if self.action == "retrieve":
            return PostRetrieveSerializer
        return PostSerializer

    def get_queryset(self):
        queryset = self.queryset
        username = self.request.query_params.get("username")
        title = self.request.query_params.get("title")
        year = self.request.query_params.get("year")
        month = self.request.query_params.get("month")
        day = self.request.query_params.get("day")
        if username:
            queryset = queryset.filter(author__username__icontains=username)
        if title:
            queryset = queryset.filter(title__icontains=title)
        if year:
            queryset = queryset.filter(published_date__year=year)

        if month:
            queryset = queryset.filter(published_date__month=month)

        if day:
            queryset = queryset.filter(published_date__day=day)
        if self.action in ("list", "retrieve"):
            return queryset.select_related("author")
        return queryset

    @extend_schema(
        methods=["GET"],
        summary="Get list of all posts",
        description="User can get a list of all posts",
        parameters=[
            OpenApiParameter(
                name="username",
                description="Filter by post author username",
                type=str,
                examples=[OpenApiExample("Example")],
            ),
            OpenApiParameter(
                name="title",
                description="Filter by post title",
                type=str,
                examples=[OpenApiExample("Example")],
            ),
            OpenApiParameter(
                name="year",
                description="Filter by post creation year",
                type=str,
                examples=[OpenApiExample("Example")],
            ),
            OpenApiParameter(
                name="month",
                description="Filter by post creation month",
                type=str,
                examples=[OpenApiExample("Example")],
            ),
            OpenApiParameter(
                name="day",
                description="Filter by post creation day",
                type=str,
                examples=[OpenApiExample("Example")],
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Add comment to a specific post",
        description="User can leave a comment on a specific post",
    )
    @action(
        detail=True,
        methods=["post"],
        url_path="add-comment",
    )
    def add_comment(self, request, pk=None):
        post = self.get_object()
        serializer = CreateCommentSerializer(
            data=request.data,
            context={"request": request, "post_id": pk},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(post=post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="Add like to a specific post",
        description="User can leave a like on a specific post",
    )
    @action(detail=True, methods=["post"], url_path="like-post")
    def like_post(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        serializer = CreateLikeSerializer(
            data=request.data,
            context={"request": request, "post_id": pk},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(post=post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="Unlike a specific post",
        description="User can unlike a specific post",
    )
    @action(detail=True, methods=["post"], url_path="unlike-post")
    def unlike_post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like = Like.objects.get(user=request.user, post=post)
        like.delete()
        return Response({"detail": "Post unliked."}, status=status.HTTP_204_NO_CONTENT)


@extend_schema_view(
    destroy=extend_schema(
        summary="Delete a comment",
        description="Admin can delete a specific comment",
    ),
)
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
        return CommentRetrieveSerializer

    @extend_schema(
        methods=["GET"],
        summary="Get list of all comments",
        description="User can get a list of all comments",
        parameters=[
            OpenApiParameter(
                name="username",
                description="Filter by comment author username",
                type=str,
                examples=[OpenApiExample("Example")],
            ),
            OpenApiParameter(
                name="year",
                description="Filter by comment creation year",
                type=str,
                examples=[OpenApiExample("Example")],
            ),
            OpenApiParameter(
                name="month",
                description="Filter by comment creation month",
                type=str,
                examples=[OpenApiExample("Example")],
            ),
            OpenApiParameter(
                name="day",
                description="Filter by comment creation day",
                type=str,
                examples=[OpenApiExample("Example")],
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


@extend_schema_view(
    destroy=extend_schema(
        summary="Delete a like",
        description="Admin can delete a specific like",
    ),
)
class LikeViewSet(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return LikeListSerializer
        return LikeRetrieveSerializer

    def get_queryset(self):
        queryset = self.queryset
        username = self.request.query_params.get("username")
        if username:
            queryset = queryset.filter(user__username__icontains=username)
        if self.action in ("list", "retrieve"):
            return queryset.select_related("user", "post")
        return queryset

    @extend_schema(
        methods=["GET"],
        summary="Get list of all likes",
        description="User can get a list of all likes",
        parameters=[
            OpenApiParameter(
                name="username",
                description="Filter by like author username",
                type=str,
                examples=[OpenApiExample("Example")],
            )
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


@extend_schema_view(
    destroy=extend_schema(
        summary="Delete a follow",
        description="Admin can delete a specific follow",
    ),
)
class FollowViewSet(ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return FollowListSerializer
        return FollowRetrieveSerializer

    def get_queryset(self):
        queryset = self.queryset
        follower = self.request.query_params.get("follower")
        followed_user = self.request.query_params.get("followed")
        if follower:
            queryset = queryset.filter(
                follower__username__icontains=follower
            )
        if followed_user:
            queryset = queryset.filter(
                followed_user__username__icontains=followed_user
            )
        if self.action in ("list", "retrieve"):
            return queryset.select_related("follower", "followed_user")
        return queryset

    @extend_schema(
        methods=["GET"],
        summary="Get list of all follows",
        description="User can get a list of all follows",
        parameters=[
            OpenApiParameter(
                name="follower",
                description="Filter by follower username",
                type=str,
                examples=[OpenApiExample("Example")],
            ),
            OpenApiParameter(
                name="followed_user",
                description="Filter by followed user username",
                type=str,
                examples=[OpenApiExample("Example")],
            )
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class FollowUserView(generics.GenericAPIView, mixins.CreateModelMixin):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    @extend_schema(
        methods=["POST"],
        summary="Follow a specific user",
        description="User can follow a specific user",
    )
    def post(self, request, *args, **kwargs):
        username = kwargs.get("username")
        followed_user = get_object_or_404(get_user_model(), username=username)
        follower = request.user
        follow_data = {"follower": follower.id, "followed_user": followed_user.id}
        serializer = self.get_serializer(data=follow_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Followed successfully"}, status=status.HTTP_201_CREATED
        )


class UnfollowUserView(generics.GenericAPIView, mixins.CreateModelMixin):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    @extend_schema(
        methods=["DELETE"],
        summary="Unfollow a specific user",
        description="User can unfollow a specific user",
    )
    def delete(self, request, *args, **kwargs):
        username = kwargs.get("username")
        followed_user = get_object_or_404(get_user_model(), username=username)
        follower = request.user
        follow_instance = Follow.objects.filter(
            follower=follower, followed_user=followed_user
        ).first()
        if follow_instance:
            follow_instance.delete()

        return Response(
            {"detail": "Unfollowed successfully"}, status=status.HTTP_204_NO_CONTENT
        )
