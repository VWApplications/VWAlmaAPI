from django.utils.translation import ugettext_lazy as _
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import status
from django.contrib.auth import get_user_model
from common.utils import convert_to_json
from accounts.enum import PermissionSet
from core.views import CustomPagination
from disciplines.models import Discipline
from . import serializers
from .models import Group
from django.db.models import Q
import logging

User = get_user_model()


class GroupViewSet(ModelViewSet):
    """
    View para gerenciar disciplinas.
    """

    pagination_class = CustomPagination

    def change_action(self):
        """
        Modifica a action para list caso precise.
        """

        if self.action == 'create' and "disciplineID" in self.request.data.keys():
            self.action = "list"

    def get_permissions(self):
        """
        Instancia e retorna a lista de permissões que essa ação requer.
        """

        self.change_action()
        
        logging.info(f"###### Action disparada: {self.action} ######")

        if self.action == 'list' or self.action == 'create':
            permission_classes = (IsAuthenticated,)
        elif self.action == 'retrieve':
            permission_classes = (IsAuthenticated,)
        else:
            permission_classes = (IsAuthenticated,)

        logging.info(f"Permissões disparadas: {permission_classes}")

        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        """
        Se for passado o atributo disciplineID irá listar
        os grupos da disciplina, caso contrário irá criar
        um novo grupo.
        """

        logging.info(f"Payload: {request.data}")

        if "disciplineID" in request.data.keys():
            logging.info("Listando grupos da disciplina.")
            return super(GroupViewSet, self).list(request, *args, **kwargs)

        logging.info("Criando um novo grupo.")
        return super(GroupViewSet, self).create(request, *args, **kwargs)

    def get_discipline(self):
        """
        Pega a disciplina passada por parâmetro.
        """

        disciplineID = self.request.data.get('disciplineID', None)

        try:
            discipline = Discipline.objects.get(id=disciplineID)
            logging.info(f"Disciplina: {convert_to_json(discipline)}")
        except Discipline.DoesNotExist:
            return False

        return discipline

    def get_queryset(self):
        """
        Pega a lista de os grupos de uma determinada disciplina.
        """

        discipline = self.get_discipline()

        if discipline:
            logging.info("Pegando os grupos da disciplina.")
            return Group.objects.filter(discipline=discipline)

        logging.info("Pegando todos os grupos.")
        return Group.objects.all()

    def get_serializer_class(self):
        """
        Retorna a classe de serialização de acordo com o tipo
        de ação disparado.
        """

        logging.info(f"Serializer: GroupSerializer")

        return serializers.GroupSerializer
