from rest_framework.permissions import BasePermission
from core.permissions import is_read_mode, is_logged, is_admin
import logging


class UpdateOwnProfile(BasePermission):
    """
    Permite os usuário editarem seu próprio perfil.
    """

    def has_object_permission(self, request, view, obj):
        if is_read_mode(request):
            logging.info("Permitido: Modo leitura.")
            return True

        if is_admin(request):
            logging.info("Permitido: Usuário administrador.")
            return True

        if is_owner(request, obj):
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
        if is_read_mode(request) or not is_logged(request):
            logging.info("Permitido: Modo leitura ou o usuário não está logado.")
            return True

        if is_logged(request) and is_admin(request):
            logging.info("Permitido: Usuário logado e administrador.")
            return True

        logging.warning("Permissão Negada.")

        return False


def is_owner(request, obj):
    """
    Verifica se o ID do usuário passado é o ID do usuário logado no sistema.
    """

    return obj.id == request.user.id