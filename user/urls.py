from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import CreateUserView, ManageUserView, LogoutUserView, MyTokenObtainPairView, UserListView, UserDetailView

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("me/", ManageUserView.as_view(), name="manage_user"),
    path("me/logout", LogoutUserView.as_view(), name="logout-user"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("users/", UserListView.as_view(), name="users-list"),
    path("users/<str:username>/", UserDetailView.as_view(), name="users-detail")
]

app_name = "user"
