from rest_framework.permissions import BasePermission
from common.permissions import GenericPermission
import logging


class OnlyLoggedTeacherCanCreateDiscipline(BasePermission):
    """
    Permite somente professor criar disciplinas.
    """

    def has_permission(self, request, view):
        perm = GenericPermission(request)

        if perm.is_teacher() or perm.is_read_mode():
            logging.info("Permitido: Modo leitura ou usuário professor.")
            return True

        logging.warning("Permissão Negada.")

        return False


class SearchDiscipline(BasePermission):
    """
    Permissão para pesquisar disciplinas.
    """

    def has_permission(self, request, view):
        perm = GenericPermission(request)

        if perm.is_read_mode() and not perm.is_teacher():
            logging.info("Permitido: Modo leitura e usuário estudante.")
            return True

        logging.warning("Permissão Negada.")

        return False


class EnterDiscipline(BasePermission):
    """
    Permissão para entrar em uma disciplina.
    """

    def has_permission(self, request, view):
        perm = GenericPermission(request)

        if not perm.is_teacher():
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
        perm = GenericPermission(request, obj)

        if perm.is_inside_discipline():
            logging.info("Permitido: Usuário é professor, aluno ou monitor da disciplina.")
            return True

        logging.warning("Permissão Negada.")

        return False


class UpdateYourOwnDisciplines(BasePermission):
    """
    Permita que apenas o professor específico que criou uma disciplina a atualize ou exclua.
    """

    def has_object_permission(self, request, view, obj):
        perm = GenericPermission(request, obj)

        if perm.is_owner():
            logging.info("Permitido: Usuário é dono da disciplina.")
            return True

        logging.warning("Permissão Negada.")

        return False
