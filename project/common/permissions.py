from rest_framework.permissions import SAFE_METHODS
from accounts.enum import PermissionSet
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

    def is_teacher(self):
        """
        Verifique se o usuário conectado é professor.
        """

        return self.request.user.permission == PermissionSet.TEACHER.value

    def is_discipline_student(self):
        """
        Verifica se o usuário é estudante da disciplina.
        """

        return self.request.user in self.obj.students.all() and not self.is_teacher()

    def is_discipline_monitor(self):
        """
        Verifica se o usuário é monitor da disciplina.
        """

        return self.request.user in self.obj.monitors.all() and not self.is_teacher()


    def is_user_owner(self):
        """
        Verifica se o usuário é ele mesmo.
        """

        return self.obj == self.request.user

    def is_owner(self):
        """
        Ele verificará se o ID do professor da disciplina que eles
        estão tentando atualizar é o objeto do professor autenticado,
        seu próprio objeto.
        """

        return self.obj.teacher == self.request.user and self.is_teacher()


    def is_inside_discipline(self):
        """
        Verifica se o usuário está dentro da disciplina.
        """

        return self.is_discipline_student() or self.is_discipline_monitor() or self.is_owner()
