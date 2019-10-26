from common.generic_view import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from common.utils import convert_to_json
from common import permissions
from . import serializers
from .models import Question
import logging


class QuestionViewSet(GenericViewSet):
    """
    View para gerenciar questões.
    """

    serializer_class = serializers.QuestionSerializer

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
        elif self.action == 'create':
            permission_classes = (IsAuthenticated, permissions.CreateSomethingInYourOwnDisciplines)
        else:
            permission_classes = (IsAuthenticated, permissions.UpdateYourOwnDisciplines)

        logging.info(f"Permissões disparadas: {permission_classes}")

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Pega a lista de os grupos de uma determinada disciplina.
        """

        section = self.get_section()

        if section:
            logging.info("Pegando as questões da seção.")
            return Question.objects.filter(section=section)

        logging.info("Pegando todas as questões.")
        return Question.objects.all()
