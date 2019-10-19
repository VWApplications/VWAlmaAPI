from rest_framework.permissions import BasePermission
from core.permissions import is_read_mode, is_teacher
import logging


class OnlyLoggedTeacherCanCreateDiscipline(BasePermission):
    """
    Permite somente professor criar disciplinas.
    """

    def has_permission(self, request, view):
        if is_teacher(request) or is_read_mode(request):
            logging.info("Permitido: Modo leitura ou usuário professor.")
            return True

        logging.warning("Permissão Negada.")

        return False


class SearchDiscipline(BasePermission):
    """
    Permissão para pesquisar disciplinas.
    """

    def has_permission(self, request, view):
        if is_read_mode(request) and not is_teacher(request):
            logging.info("Permitido: Modo leitura e usuário estudante.")
            return True

        logging.warning("Permissão Negada.")

        return False


class EnterDiscipline(BasePermission):
    """
    Permissão para entrar em uma disciplina.
    """

    def has_permission(self, request, view):
        if not is_teacher(request):
            logging.info("Permitido: Usuário estudante.")
            return True

        logging.warning("Permissão Negada.")

        return False


class SeeDiscipline(BasePermission):
    """
    Permite que um aluno só veja a disciplina se ele estiver dentro
    da disciplina.
    """

    def has_object_permission(self, request, view, obj):
        if request.user in obj.students.all() or request.user in obj.monitors.all():
            logging.info("Permitido: Usuário é aluno ou monitor da disciplina.")
            return True

        logging.warning("Permissão Negada.")

        return False


class UpdateYourOwnDisciplines(BasePermission):
    """
    Permita que apenas o professor específico que criou uma disciplina a atualize ou exclua.
    """

    def has_object_permission(self, request, view, obj):
        if is_owner(request, obj):
            logging.info("Permitido: Usuário é dono da disciplina.")
            return True

        logging.warning("Permissão Negada.")

        return False


def is_owner(request, obj):
    """
    Ele verificará se o ID do professor da disciplina que eles
    estão tentando atualizar é o objeto do professor autenticado,
    seu próprio objeto.
    """

    return obj.teacher.id == request.user.id
