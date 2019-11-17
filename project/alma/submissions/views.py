from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.decorators import action
from rest_framework.views import status
from common.generic_view import GenericViewSet
from common import permissions
from alma.sections.models import Section
from alma.accounts.models import AlmaUser
from alma.accounts.enum import AlmaPermissionSet
from . import serializers
from .tasks import calculate_score
from .enum import ExamSet
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

        if self.action == 'list' or self.action == 'retrieve' or self.action == 'destroy':
            permission_classes = (IsAuthenticated, permissions.OnlyAdmin)
        elif self.action == 'send_submission':
            permission_classes = (IsAuthenticated,)
        else:
            permission_classes = (IsAuthenticated, permissions.CanNotBeDone)

        logging.info(f"Permissões disparadas: {permission_classes}")

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Pega a lista de submissões (futuramente inserir filtros)
        """

        logging.info("Pegando todas as seções.")
        return Submission.objects.all()

    @action(detail=False, methods=['post'], url_path="send", url_name="send")
    def send_submission(self, request):
        """
        Envia e cria a submissão da avaliação.
        """

        logging.info(f"Dados para criação da submissão: {request.data}")

        if "section" not in request.data.keys():
            raise ParseError("A identificação da sessão da avaliação é obrigatória.")

        if "answers" not in request.data.keys():
            raise ParseError("O JSON de respostas é obrigatório.")

        if "student" not in request.data.keys():
            raise ParseError("O identificação do estudante que submeteu as respostas é obrigatório.")

        if request.data['exam'] not in [item.value for item in ExamSet]:
            raise ParseError("Tipo de avaliação inexistente.")

        if not Section.objects.filter(id=request.data['section']).exists():
            raise ParseError("Sessão não encontrada.")

        if not AlmaUser.objects.filter(id=request.data['student'], permission=AlmaPermissionSet.STUDENT.value).exists():
            raise ParseError("Estudante não encontrado.")

        calculate_score(request.data)

        return Response({"success": True}, status=status.HTTP_200_OK)
