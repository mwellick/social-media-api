from django.contrib.auth import logout
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import UserSerializer, UserRetrieveSerializer, UserLogoutSerializer, MyTokenObtainPairSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200 and not request.user.is_anonymous:
            user = request.user
            user.online = True
            user.save()
        return response


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserRetrieveSerializer

    def get_object(self):
        return self.request.user


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
