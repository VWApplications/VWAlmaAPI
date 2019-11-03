from rest_framework.permissions import SAFE_METHODS


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
