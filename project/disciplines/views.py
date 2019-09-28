from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .serializers import DisciplineSerializer
from .permissions import (
    OnlyLoggedTeacherCanCreateDiscipline,
    UpdateYourOwnDisciplines
)
from .models import Discipline
import logging


class DisciplineViewSet(ModelViewSet):
    """
    View para gerenciar disciplinas.
    """

    queryset = Discipline.objects.all()
    serializer_class = DisciplineSerializer

    def get_permissions(self):
        """
        Instancia e retorna a lista de permissões que essa ação requer.

        Ações: list, create, destroy, retrieve, update, partial_update
        """

        logging.info("Action disparada: " + str(self.action))

        if self.action == 'list' or self.action == 'create':
            permission_classes = (OnlyLoggedTeacherCanCreateDiscipline,)
        else:
            permission_classes = (IsAuthenticated, UpdateYourOwnDisciplines,)

        logging.info("Permissões disparadas: " + str(permission_classes))

        return [permission() for permission in permission_classes]
