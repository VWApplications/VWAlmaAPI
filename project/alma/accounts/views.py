from django.utils.translation import ugettext_lazy as _
from rest_framework.views import status, APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from accounts import permissions
from .models import AlmaUser
from . import serializers
import logging


class AlmaUserViewSet(ModelViewSet):
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

        logging.info("Query Parametros: " + str({'name': name, 'email': email}))

        users = AlmaUser.objects.all()

        if name:
            users = users.filter(user__name__icontains=name)
            logging.info(f"Filtrando por nome: {users}")

        if email:
            users = users.filter(user__email__icontains=email)
            logging.info(f"Filtrando por email: {users}")

        return users

    def get_serializer_class(self):
        """
        Retorna a classe de serialização de acordo com o tipo
        de ação disparado.
        """

        logging.info(f"Action disparada: {self.action}")

        if self.action == 'list' or self.action == 'create':
            logging.info("Entrando no AlmaUserRegisterSerializer.")
            return serializers.AlmaUserRegisterSerializer

        logging.info("Entrando no AlmaUserSerializer.")

        return serializers.AlmaUserSerializer

    def get_permissions(self):
        """
        Instancia e retorna a lista de permissões de acordo com a ação disparada.
        """

        if self.action == 'list' or self.action == 'create':
            permission_classes = (permissions.CreateListUserPermission,)
        else:
            permission_classes = (IsAuthenticated, permissions.UpdateOwnProfile)

        logging.info(f"Permissões disparadas: {permission_classes}")

        return [permission() for permission in permission_classes]


class UserUploadPhotoView(APIView):
    """
    Classe reponsável por armazenar a foto do usuário.
    """

    parser_class = (FileUploadParser,)

    def put(self, request, *args, **kwargs):
        """
        Requisição para armazenar o arquivo.
        """

        logging.info("Atualizando a foto do usuário")

        if 'photo' not in request.data:
            raise ParseError(_("Empty content."))

        img = request.data['photo']
        filename = self.kwargs['filename'].replace(" ", "_")

        logging.info("Foto {0}: {1}".format(filename, str(img)))

        request.user.alma_user.photo.save(filename, img, save=True)

        logging.info("Foto atualizada com sucesso!")

        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        """
        Remove a foto do usuário.
        """

        request.user.alma_user.photo.delete(save=True)
        return Response(status=status.HTTP_204_NO_CONTENT)