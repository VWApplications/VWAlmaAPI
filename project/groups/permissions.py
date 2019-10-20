from rest_framework.permissions import BasePermission
from common.permissions import GenericPermission
import logging


class SeePage(BasePermission):
    """
    Permite que um aluno só veja a disciplina se ele estiver dentro
    da disciplina.
    """

    def has_permission(self, request, view):
        perm = GenericPermission(request, view.get_discipline())

        if perm.is_inside_discipline():
            logging.info("Permitido: Usuário é professor, aluno ou monitor da disciplina.")
            return True

        logging.warning("Permissão Negada.")

        return False

    def has_object_permission(self, request, view, obj):
        perm = GenericPermission(request, obj.discipline)

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
        perm = GenericPermission(request, obj.discipline)

        if perm.is_owner():
            logging.info("Permitido: Usuário é dono da disciplina.")
            return True

        logging.warning("Permissão Negada.")

        return False
