from rest_framework.permissions import BasePermission
from common.permissions import GenericPermission
import logging


class CreateUpdateDestroyAdminPermission(BasePermission):
    """
    Só permite realizar essas operações se o usuário tiver logado
    no sistema e for administrador.
    """

    def has_permission(self, request, view):
        perm = GenericPermission(request)

        if perm.is_read_mode():
            logging.info("Permitido: Modo leitura.")
            return True

        if perm.is_logged() and perm.is_admin():
            logging.info("Permitido: Usuário administrador logado.")
            return True

        logging.warning("Permissão Negada.")

        return False
