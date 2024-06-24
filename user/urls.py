from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    CreateUserView,
    ManageUserView,
    LogoutUserView,
    MyTokenObtainPairView,
    UserListView,
    UserDetailView,
)
from api.views import FollowUserView, UnfollowUserView

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(
        "me/",
        ManageUserView.as_view(
            actions={
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="manage_user",
    ),
    path("me/logout", LogoutUserView.as_view(), name="logout-user"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("users/", UserListView.as_view(actions={"get": "list"}), name="users-list"),
    path(
        "<str:username>/",
        UserDetailView.as_view(actions={"get": "retrieve"}),
        name="users-detail",
    ),
    path("<str:username>/follow/", FollowUserView.as_view(), name="follow-user"),
    path("<str:username>/unfollow/", UnfollowUserView.as_view(), name="follow-user"),
]

app_name = "user"
