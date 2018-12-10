from rest_framework import filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    DisciplineSerializer,
)
from .permissions import (
    OnlyLoggedTeacherCanCreateDiscipline,
    UpdateYourOwnDisciplines
)
from .models import Discipline


class DisciplineViewSet(ModelViewSet):
    """
    View set to manage disciplines.
    """

    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'course', 'classroom', 'teacher')
    ordering = ('title',)

    queryset = Discipline.objects.all()
    serializer_class = DisciplineSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.

        actions: list, create, destroy, retrieve, update, partial_update
        """

        if self.action == 'list' or self.action == 'create':
            permission_classes = (OnlyLoggedTeacherCanCreateDiscipline,)
        else:
            permission_classes = (IsAuthenticated, UpdateYourOwnDisciplines,)

        return [permission() for permission in permission_classes]
