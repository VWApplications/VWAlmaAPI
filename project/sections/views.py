from common.generic_view import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from common.utils import convert_to_json
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import status
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

        discipline = self.get_discipline()

        if discipline:
            logging.info("Pegando os grupos da disciplina.")
            if self.request.user == discipline.teacher:
                return Section.objects.filter(discipline=discipline)
            else:
                return Section.objects.filter(discipline=discipline, is_closed=False)

        logging.info("Pegando todos os grupos.")
        return Section.objects.all()

    @action(detail=True, methods=['get'], url_path="provide", url_name="provide")
    def provide_section(self, request, pk):
        """
        Libera ou Fecha o seção da disciplina para visualização.
        """

        logging.info(f"Payload: pk={pk}")

        section = self.get_object()
        logging.info(f"Seção: {convert_to_json(section)}")

        section.is_closed = not section.is_closed
        section.save()

        return Response({"success": True}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path="finish", url_name="finish")
    def finish_section(self, request, pk):
        """
        Finaliza ou Começa a seção da disciplina.
        """

        logging.info(f"Payload: pk={pk}")

        section = self.get_object()
        logging.info(f"Seção: {convert_to_json(section)}")

        section.is_finished = not section.is_finished

        if section.is_finished:
            section.is_closed = True
        else:
            section.is_closed = False

        section.save()

        return Response({"success": True}, status=status.HTTP_200_OK)
