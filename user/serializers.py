from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils.translation import gettext as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "email",
            "password",
            "username"
        ]
        read_only_fields = [
            "id",
            "is_staff"
        ]
        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 5,
                "style": {"input_type": "password"},
                "label": _("Password"),
            }
        }

    def create(self, validated_data):
        """User creation with encrypted password"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """User update with encrypted password"""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "email",
            "username"
        ]


class UserRetrieveSerializer(serializers.ModelSerializer):
    followers = serializers.IntegerField(
        source="user_followers.count", read_only=True
    )
    users_followed = serializers.IntegerField(
        source="user_following.count", read_only=True
    )

    class Meta:
        model = get_user_model()
        fields = [
            "email",
            "username",
            "online",
            "bio",
            "followers",
            "users_followed",
            "profile_image"
        ]


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        user.online = True
        user.save()
        return data


class UserLogoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "email",
            "password"
        ]
        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 5,
                "style": {"input_type": "password"},
                "label": _("Password"),
            }
        }
