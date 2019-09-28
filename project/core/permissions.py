from rest_framework.permissions import BasePermission, SAFE_METHODS
import logging


class CreateUpdateDestroyAdminPermission(BasePermission):
    """
    Permissão de edição, criação e remoção de notícias.
    """

    def has_permission(self, request, view):
        """
        Só permite realizar essas operações se o usuário
        tiver logado no sistema e for administrador.
        """

        if is_read_mode(request):
            logging.info("Permitido: Modo leitura.")
            return True

        if is_logged(request) and is_admin(request):
            logging.info("Permitido: Usuário administrador logado.")
            return True

        logging.info("Permissão Negada.")

        return False


def is_read_mode(request):
    """
    Método de lista e recuperação, somente modo de leitura (métodos seguros)
    """

    logging.info("Método de requisição: " + request.method)

    if request.method in SAFE_METHODS:
        return True

    return False


def is_logged(request):
    """
    Verifique se o usuário está logado ou não
    """

    return request.user and request.user.is_authenticated


def is_admin(request):
    """
    Verifique se o usuário é administrador
    """

    return request.user.is_staff


def is_teacher(request):
    """
    Verifique se o usuário conectado é professor.
    """

    is_teacher = False

    if is_logged(request):
        is_teacher = request.user.is_teacher

    return is_teacher
