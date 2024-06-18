from rest_framework import generics
from rest_framework.permissions import AllowAny

from .serializers import UserSerializer, UserRetrieveSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserRetrieveSerializer

    def get_object(self):
        return self.request.user
