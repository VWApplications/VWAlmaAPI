from rest_framework.permissions import BasePermission
from alma.accounts.enum import AlmaPermissionSet
from common.permissions import GenericPermission
import logging


class GenericAlmaPermission:
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

    def is_teacher(self):
        """
        Verifique se o usuário conectado é professor.
        """

        return self.request.user.alma_user.permission == AlmaPermissionSet.TEACHER.value

    def is_discipline_student(self):
        """
        Verifica se o usuário é estudante da disciplina.
        """

        return self.request.user.alma_user in self.obj.students.all() and not self.is_teacher()

    def is_discipline_monitor(self):
        """
        Verifica se o usuário é monitor da disciplina.
        """

        return self.request.user.alma_user in self.obj.monitors.all() and not self.is_teacher()

    def is_discipline_owner(self):
        """
        Ele verificará se o ID do professor da disciplina que eles
        estão tentando atualizar é o objeto do professor autenticado,
        seu próprio objeto.
        """

        return self.obj.teacher == self.request.user.alma_user and self.is_teacher()

    def is_inside_discipline(self):
        """
        Verifica se o usuário está dentro da disciplina.
        """

        return self.is_discipline_student() or self.is_discipline_monitor() or self.is_discipline_owner()


class SeePage(BasePermission):
    """
    Permite que um aluno só veja páginas se ele estiver dentro
    da disciplina.
    """

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True

        section = view.get_section()
        if not section:
            discipline = view.get_discipline()
        else:
            discipline = section.discipline

        if not discipline:
            return False

        perm = GenericAlmaPermission(request, discipline)

        if perm.is_inside_discipline():
            logging.info("Permitido: Usuário é professor, aluno ou monitor da disciplina.")
            return True

        logging.warning("Permissão Negada.")

        return False


class SeeObjPage(BasePermission):
    """
    Permite que um aluno só veja páginas se ele estiver dentro
    da disciplina.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        try:
            perm = GenericAlmaPermission(request, obj.discipline)
        except AttributeError:
            perm = GenericAlmaPermission(request, obj.section.discipline)

        if perm.is_inside_discipline():
            logging.info("Permitido: Usuário é professor, aluno ou monitor da disciplina.")
            return True

        logging.warning("Permissão Negada.")

        return False


class CreateSomethingInYourOwnDisciplines(BasePermission):
    """
    Permite criar algo somente se o professor for dono da disciplina.
    """

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True

        section = view.get_section()
        if not section:
            discipline = view.get_discipline()
        else:
            discipline = section.discipline

        if not discipline:
            return False

        perm = GenericAlmaPermission(request, discipline)

        if perm.is_discipline_owner():
            logging.info("Permitido: Usuário é dono da disciplina.")
            return True

        logging.warning("Permissão Negada.")

        return False


class UpdateYourOwnDisciplines(BasePermission):
    """
    Permita que apenas o professor específico que criou uma disciplina a atualize ou exclua.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        try:
            perm = GenericAlmaPermission(request, obj.discipline)
        except AttributeError:
            perm = GenericAlmaPermission(request, obj.section.discipline)

        if perm.is_discipline_owner():
            logging.info("Permitido: Usuário é dono da disciplina.")
            return True

        logging.warning("Permissão Negada.")

        return False
