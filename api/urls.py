from django.urls import path, include
from rest_framework import routers
from .views import (
    PostViewSet,
    CommentViewSet,
    LikeViewSet,
    FollowViewSet,
    FollowUserView,
    UnfollowUserView,
)

router = routers.DefaultRouter()
router.register("posts", PostViewSet)
router.register("comments", CommentViewSet)
router.register("likes", LikeViewSet)
router.register("follows", FollowViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("follow-user/", FollowUserView.as_view(), name="follow-user"),
    path("unfollow-user/", UnfollowUserView.as_view(), name="unfollow-user"),
]

app_name = "social_media_api"
