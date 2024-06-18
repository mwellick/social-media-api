from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils.translation import gettext as _


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


class UserRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "email",
            "username",
            "bio",
            "user_followers",
            "user_following",
            "profile_image"
        ]
