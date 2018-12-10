from rest_framework.permissions import BasePermission
from core.permissions import (
    is_read_mode, is_logged, is_teacher
)


class OnlyLoggedTeacherCanCreateDiscipline(BasePermission):
    """
    Allow only teacher to create disciplines.
    """

    def has_permission(self, request, view):

        if is_teacher(request) or is_read_mode(request):
            return True

        return False


class UpdateYourOwnDisciplines(BasePermission):
    """
    Allow only the specific teacher that created a discipline to update or
    delete it.
    """

    def has_object_permission(self, request, view, obj):
        can_update = False

        if is_logged(request):
            can_update = is_owner(request, obj)

        if can_update or is_read_mode(request):
            return True

        return False


def is_owner(request, obj):
    """
    It will check if the object ID that they're trying to update
    is the authenticated teacher object, their own object.
    """

    return obj.teacher.id == request.user.id
