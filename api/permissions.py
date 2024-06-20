from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminAllORIsAuthenticatedOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):

        return bool(
            (
                request.method in SAFE_METHODS
                and request.user
                and request.user.is_authenticated
            )
            or obj.author == request.user or request.user.is_staff
        )
