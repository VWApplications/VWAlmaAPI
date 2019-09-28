from rest_framework.views import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .serializers import (
    UserSerializer, UserRegisterSerializer, UserPasswordSerializer
)
from django.contrib.auth import get_user_model
from .permissions import UpdateOwnProfile, CreateListUserPermission
import logging

User = get_user_model()


class UserViewSet(ModelViewSet):
    """
    Views de usuários.
    """

    def get_queryset(self):
        """
        Filtro de usuário por meio de query string.
        """

        logging.info("Buscando os usuários")

        name = self.request.query_params.get('name', None)
        email = self.request.query_params.get('email', None)

        logging.info("Query Parametros: " + str({"name": name, "email": email}))

        users = User.objects.all()

        if name:
            users = users.filter(name__icontains=name)
            logging.info("Filtrando por nome: " + str(users))

        if email:
            users = users.filter(email__icontains=email)
            logging.info("Filtrando por email: " + str(users))

        return users

    def get_serializer_class(self):
        """
        Retorna a classe de serialização de acordo com o tipo
        de ação disparado.

        ações: list, create, destroy, retrieve, update, partial_update
        """

        logging.info("Action disparada: " + str(self.action))

        if self.action == 'list' or self.action == 'create':
            logging.info("Entrando no UserRegisterSerializer.")
            return UserRegisterSerializer
        elif self.action == 'set_password':
            logging.info("Entrando no UserPasswordSerializer.")
            return UserPasswordSerializer

        logging.info("Entrando no UserSerializer.")

        return UserSerializer

    def get_permissions(self):
        """
        Instancia e retorna a lista de permissões de acordo com a ação disparada.

        ações: list, create, destroy, retrieve, update, partial_update
        """

        if self.action == 'list' or self.action == 'create':
            permission_classes = (CreateListUserPermission,)
        else:
            permission_classes = (IsAuthenticated, UpdateOwnProfile)

        logging.info("Permissões disparadas: " + str(permission_classes))

        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'], url_path="current_user", url_name="current-user")
    def current_user(self, request):
        """
        Pega o usuário autenticado.
        """

        logging.info("Pegando o usuário logado: " + str(request.user))

        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['put', 'patch'], url_path="change_password", url_name="change-password")
    def set_password(self, request):
        """
        Controlador que permite que um usuário conectado edite sua própria senha.
        """

        logging.info("Atualizando senha do usuário")

        logging.info("Usuário: " + str(request.user))

        serializer = self.get_serializer(request.user, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.update(request.user, request.data)
            return Response({'success': True}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)