from common.generic_view import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from common import permissions
from . import serializers
from .models import Section
import logging


class SectionViewSet(GenericViewSet):
    """
    View para gerenciar disciplinas.
    """

    serializer_class = serializers.SectionSerializer

    def get_permissions(self):
        """
        Instancia e retorna a lista de permissões que essa ação requer.
        """

        self.change_action()

        logging.info(f"###### Action disparada: {self.action} ######")

        if self.action == 'list':
            permission_classes = (IsAuthenticated, permissions.SeePage)
        elif self.action == 'retrieve':
            permission_classes = (IsAuthenticated, permissions.SeeObjPage)
        else:
            permission_classes = (IsAuthenticated, permissions.UpdateYourOwnDisciplines)

        logging.info(f"Permissões disparadas: {permission_classes}")

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Pega a lista de os grupos de uma determinada disciplina.
        """

        discipline = self.get_discipline()

        if discipline:
            logging.info("Pegando os grupos da disciplina.")
            return Section.objects.filter(discipline=discipline)

        logging.info("Pegando todos os grupos.")
        return Section.objects.all()
