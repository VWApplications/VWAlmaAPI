from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import status
from common.utils import convert_to_json
from common.generic_view import GenericViewSet
from common import permissions
from alma.core.permissions import SeePage
from . import serializers
from .models import Submission
import logging


class SubmissionViewSet(GenericViewSet):
    """
    View para gerenciar submissões.
    """

    serializer_class = serializers.SubmissionSerializer

    def get_permissions(self):
        """
        Instancia e retorna a lista de permissões que essa ação requer.
        """

        self.change_action()

        logging.info(f"###### Action disparada: {self.action} ######")

        if self.action == 'list' or self.action == 'retrieve' or self.action == 'delete':
            # Só o administrador pode ver
            permission_classes = (IsAuthenticated, permissions.OnlyAdmin)
        elif self.action == 'create':
            # Qualquer um pode criar submissões (validação dentro do create)
            permission_classes = (IsAuthenticated, SeePage)
        else:
            # Não se pode editar uma submissão.
            permission_classes = (IsAuthenticated, permissions.CanNotBeDone)

        logging.info(f"Permissões disparadas: {permission_classes}")

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Pega a lista de submissões (futuramente inserir filtros)
        """

        logging.info("Pegando todas as seções.")
        return Submission.objects.all()
