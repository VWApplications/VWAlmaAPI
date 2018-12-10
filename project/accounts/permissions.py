from rest_framework.permissions import BasePermission, SAFE_METHODS
from core.permissions import (
    is_read_mode, is_logged, is_admin
)


class UpdateOwnProfile(BasePermission):
    """
    Allow users to edit their own profile.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check user is trying to edit their own profile.
        """

        if is_read_mode(request):
            return True

        return is_owner(request, obj)


class CreateListUserPermission(BasePermission):
    """
    Allow to register on system only if not authenticated
    or if user is admin.
    """

    def has_permission(self, request, view):

        if is_read_mode(request) or not is_logged(request):
            return True

        if is_logged(request) and is_admin(request):
            return True

        return False


def is_owner(request, obj):
    """
    It will check if the object ID that they're trying to update
    is the authenticated user object, their own object.
    """

    return obj.id == request.user.id