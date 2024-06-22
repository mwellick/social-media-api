from django.contrib.auth import logout, get_user_model
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .serializers import UserSerializer, UserRetrieveSerializer, UserLogoutSerializer, MyTokenObtainPairSerializer, \
    UserListSerializer


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


class ManageUserView(generics.RetrieveUpdateAPIView):
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
        return Response({
            "status": "You have logged out"},
            status=status.HTTP_204_NO_CONTENT
        )


class UserListView(generics.ListAPIView):
    serializer_class = UserListSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        email = self.request.query_params.get("email")
        username = self.request.query_params.get("username")

        if username:
            queryset = queryset.filter(username__icontains=username)
        if email:
            queryset = queryset.filter(email__icontains=email)

        return queryset


class UserDetailView(generics.RetrieveAPIView):
    queryset = get_user_model()
    permission_classes = [IsAuthenticated]
    serializer_class = UserRetrieveSerializer
    lookup_field = "username"
