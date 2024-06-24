from django.contrib.auth import logout, get_user_model
from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiParameter,
    extend_schema_view,
)
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    UserSerializer,
    UserRetrieveSerializer,
    UserLogoutSerializer,
    MyTokenObtainPairSerializer,
    UserListSerializer,
)


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200 and not request.user.is_anonymous:
            user = request.user
            user.online = True
            user.save()
        return response


@extend_schema_view(
    retrieve=extend_schema(
        summary="User profile page",
        description="User can get access to user's personal information",
    ),
    update=extend_schema(
        summary="Update user's profile page info",
        description="User can update user's personal information",
    ),
    partial_update=extend_schema(
        summary="Partial update user's profile update",
        description="User can  partially update user's personal information",
    ),
    destroy=extend_schema(
        summary="Delete account",
        description="User can delete own account",
    ),
)
class ManageUserView(ModelViewSet):
    serializer_class = UserRetrieveSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LogoutUserView(
    generics.GenericAPIView,
):
    serializer_class = UserLogoutSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        logout(request)
        user.online = False
        user.save()
        return Response(
            {"status": "You have logged out"}, status=status.HTTP_204_NO_CONTENT
        )


class UserListView(ModelViewSet):
    serializer_class = UserListSerializer

    def get_queryset(self):
        queryset = get_user_model().objects.all()
        email = self.request.query_params.get("email")
        username = self.request.query_params.get("username")

        if username:
            queryset = queryset.filter(username__icontains=username)
        if email:
            queryset = queryset.filter(email__icontains=email)

        return queryset

    @extend_schema(
        methods=["GET"],
        summary="Get list of all registered users",
        description="User can get a list of all users",
        parameters=[
            OpenApiParameter(
                name="username",
                description="Filter by user username",
                type=str,
                examples=[OpenApiExample("Example")],
            ),
            OpenApiParameter(
                name="email",
                description="Filter by user email",
                type=str,
                examples=[OpenApiExample("Example")],
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class UserDetailView(ModelViewSet):
    queryset = get_user_model()
    permission_classes = [IsAuthenticated]
    serializer_class = UserRetrieveSerializer
    lookup_field = "username"

    def get_queryset(self):
        return get_user_model().objects.prefetch_related(
            "user_followers", "user_following"
        )

    @extend_schema(
        methods=["GET"],
        summary="Get info about specific user",
        description="User can get detailed info about specific user",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
