from django.utils.translation import ugettext_lazy as _
from common.generic_view import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import status
from django.contrib.auth import get_user_model
from common.utils import convert_to_json
from accounts.enum import PermissionSet
from disciplines.models import Discipline
from . import serializers
from .models import Group
from django.db.models import Q
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

        if self.action == 'list' or self.action == 'create':
            permission_classes = (IsAuthenticated,)
        elif self.action == 'retrieve':
            permission_classes = (IsAuthenticated,)
        else:
            permission_classes = (IsAuthenticated,)

        logging.info(f"Permissões disparadas: {permission_classes}")

        return [permission() for permission in permission_classes]

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
