from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrAdminOrIfAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        user = (
            getattr(obj, "author", None)
            or getattr(obj, "user", None)
            or getattr(obj, "comment_author", None)
        )

        if request.method in ["PUT", "PATCH", "DELETE"]:
            return user == request.user or request.user.is_staff

        return bool(request.user and request.user.is_authenticated)
