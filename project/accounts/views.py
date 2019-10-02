from django.utils.translation import ugettext_lazy as _
from rest_framework.views import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from accounts.models import PasswordReset
from accounts.utils import generate_hash_key
from common.email import send_email_template
from . import serializers, permissions
from django.contrib.auth import get_user_model
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
            return serializers.UserRegisterSerializer
        elif self.action == 'set_password':
            logging.info("Entrando no UserPasswordSerializer.")
            return serializers.UserPasswordSerializer
        elif self.action == 'create_new_password':
            logging.info("Entrando no ResetPasswordSerializer")
            return serializers.ResetPasswordSerializer

        logging.info("Entrando no UserSerializer.")

        return serializers.UserSerializer

    def get_permissions(self):
        """
        Instancia e retorna a lista de permissões de acordo com a ação disparada.

        ações: list, create, destroy, retrieve, update, partial_update
        """

        if (self.action == 'list' or self.action == 'create' or
            self.action == 'reset_password' or self.action == 'create_new_password'):
            permission_classes = (permissions.CreateListUserPermission,)
        else:
            permission_classes = (IsAuthenticated, permissions.UpdateOwnProfile)

        logging.info("Permissões disparadas: " + str(permission_classes))

        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'], url_path="reset_password", url_name="reset-password")
    def reset_password(self, request):
        """
        Reseta a senha.
        """

        logging.info("Resetando a senha do usuário.")

        if "email" not in request.data:
            raise ParseError(_("Email is required."))

        try:
            user = User.objects.get(email=request.data['email'])
        except User.DoesNotExist:
            logging.info("Usuário não encontrado.")
            return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)

        # Gera a chave única para resetar a senha.
        key = generate_hash_key(user.email)
        reset_password = PasswordReset(user=user, key=key)
        reset_password.save()

        # Envia o email
        send_email_template(
            subject=_('Requesting new password'),
            template='reset_password_email.html',
            context={'reset_password': reset_password},
            recipient_list=[user.email],
        )

        return Response({'success': True}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['put'], url_path="create_new_password", url_name="create-new-password")
    def create_new_password(self, request):
        """
        Cria uma nova senha para o usuário.
        """

        logging.info("Criando uma nova senha")

        try:
            # Pega o usuário de acordo com a chave passada.
            reset = PasswordReset.objects.get(key=request.data['key'])
        except PasswordReset.DoesNotExist as error:
            logging.error(error)
            logging.warning("Não foi possível encontrar o usuário da chave passada: " + str(request.data['key']))
            raise ParseError(_("Invalid key."))

        data = {
            "new_password": request.data['new_password'],
            "confirm_password": request.data['confirm_password'],
            "reset": reset
        }

        serializer = self.get_serializer(reset.user, data=data)
        if serializer.is_valid():
            serializer.update(reset.user, data)
            return Response({'success': True}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path="current_user", url_name="current-user")
    def current_user(self, request):
        """
        Pega o usuário autenticado.
        """

        logging.info("Pegando o usuário logado: " + str(request.user))

        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['put'], url_path="change_password", url_name="change-password")
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
        filename = self.kwargs['filename']

        logging.info("Foto {0}: {1}".format(filename, str(img)))

        request.user.photo.save(filename, img, save=True)

        logging.info("Foto atualizada com sucesso!")

        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        """
        Remove a foto do usuário.
        """

        request.user.photo.delete(save=True)
        return Response(status=status.HTTP_204_NO_CONTENT)