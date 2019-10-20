from rest_framework.permissions import BasePermission
from common.permissions import GenericPermission
import logging


class UpdateOwnProfile(BasePermission):
    """
    Permite os usuário editarem seu próprio perfil.
    """

    def has_object_permission(self, request, view, obj):
        perm = GenericPermission(request, obj)

        if perm.is_read_mode():
            logging.info("Permitido: Modo leitura.")
            return True

        if perm.is_admin():
            logging.info("Permitido: Usuário administrador.")
            return True

        if perm.is_user_owner():
            logging.info("Permitido: Usuário dono do da conta.")
            return True

        logging.warning("Permissão Negada.")

        return False


class CreateListUserPermission(BasePermission):
    """
    Permite registrar no sistema somente se o usuário não tiver logado
    ou for um administrador.
    """

    def has_permission(self, request, view):
        perm = GenericPermission(request)

        if perm.is_read_mode() or not perm.is_logged():
            logging.info("Permitido: Modo leitura ou o usuário não está logado.")
            return True

        if perm.is_logged() and perm.is_admin():
            logging.info("Permitido: Usuário logado e administrador.")
            return True

        logging.warning("Permissão Negada.")

        return False
