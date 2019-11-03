from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import status
from common.generic_view import GenericViewSet
from common.utils import convert_to_json
from common import permissions
from . import serializers
from .models import Group
import logging

User = get_user_model()


class GroupViewSet(GenericViewSet):
    """
    View para gerenciar disciplinas.
    """

    serializer_class = serializers.GroupSerializer

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
                return Group.objects.filter(discipline=discipline)
            else:
                return Group.objects.filter(discipline=discipline, is_provided=True)

        logging.info("Pegando todos os grupos.")
        return Group.objects.all()

    @action(detail=True, methods=['get'], url_path="provide", url_name="provide")
    def provide_group(self, request, pk):
        """
        Libera ou Fecha o grupo da disciplina para visualização.
        """

        logging.info("Liberando o grupo da disciplina.")

        logging.info(f"Payload: pk={pk}")

        group = self.get_object()
        logging.info(f"Grupo: {convert_to_json(group)}")

        group.is_provided = not group.is_provided
        group.save()

        return Response({"success": True}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path="add_student", url_name="add-student")
    def add_student(self, request, pk):
        """
        Insere um estudante no grupo.
        """

        logging.info("Adicionando um novo estudante ao grupo.")

        group = self.get_object()
        logging.info(f"Grupo: {convert_to_json(group)}")

        data = request.data
        logging.info(f"Payload: {data}")

        if "email" not in data.keys():
            return Response({"success": False, "detail": _("Incorrect Payload.")}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student = group.discipline.students.get(email=data['email'])
        except User.DoesNotExist:
            return Response({"success": False, "detail": _("User is not part of the discipline.")}, status=status.HTTP_400_BAD_REQUEST)

        if group.students_limit <= group.students.count():
            return Response({"success": False, "detail": _("The group is full.")}, status=status.HTTP_400_BAD_REQUEST)

        for discipline_group in group.discipline.groups.all():
            if student in discipline_group.students.all():
                return Response({"success": False, "detail": _("User is already in a group.")}, status=status.HTTP_400_BAD_REQUEST)

        group.students.add(student)

        return Response({"success": True}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path="remove_student", url_name="remove-student")
    def remove_student(self, request, pk):
        """
        Remove um estudante da disciplina.
        """

        logging.info("Removendo o estudante do grupo.")

        group = self.get_object()
        logging.info(f"Grupo: {convert_to_json(group)}")

        data = request.data
        logging.info(f"Payload: {data}")

        if "id" not in data.keys():
            return Response({"success": False, "detail": _("Incorrect Payload.")}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student = group.students.get(id=data['id'])
        except User.DoesNotExist:
            return Response({"success": False, "detail": _("User isn't part of the group.")}, status=status.HTTP_400_BAD_REQUEST)

        group.students.remove(student)

        return Response({"success": True}, status=status.HTTP_200_OK)