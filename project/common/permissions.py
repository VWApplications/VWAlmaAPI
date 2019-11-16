from rest_framework.permissions import SAFE_METHODS
from rest_framework.permissions import BasePermission
import logging


class GenericPermission:
    """
    Permissões Genéricas.
    """

    def __init__(self, request, obj=None, view=None):
        """
        Construtor
        """

        self.request = request
        self.obj = obj
        self.view = view

    def is_read_mode(self):
        """
        Método de lista e recuperação, somente modo de leitura (métodos seguros)
        """

        return self.request.method in SAFE_METHODS

    def is_logged(self):
        """
        Verifique se o usuário está logado ou não
        """

        return self.request.user and self.request.user.is_authenticated

    def is_admin(self):
        """
        Verifique se o usuário é administrador
        """

        return self.request.user.is_staff

    def is_user_owner(self):
        """
        Verifica se o usuário é ele mesmo.
        """

        return self.obj == self.request.user


class OnlyAdmin(BasePermission):
    """
    Somente o administrador pode fazer isso.
    """

    def has_permission(self, request, view):
        perm = GenericPermission(request, view)

        is_admin = perm.is_admin()

        if not is_admin:
            logging.info("Sómente o administrador pode realizar essa ação.")

        return is_admin


class CanNotBeDone(BasePermission):
    """
    Não permitir a ação.
    """

    def has_permission(self, request, view):
        logging.info("Essa ação não pode ser feita.")
        return False


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