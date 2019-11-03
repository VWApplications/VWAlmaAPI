from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ParseError
from rest_framework.serializers import ModelSerializer, CharField, Serializer
from accounts.serializers import UserSerializer, UserRegisterSerializer
from .models import AlmaUser
import logging

User = get_user_model()


class AlmaUserSerializer(ModelSerializer):
    """
    O serializado para pegar os dados do usuário
    """

    user = UserSerializer()

    class Meta:
        model = AlmaUser
        fields = (
            'id', 'user', 'photo', 'permission',
            'created_at', 'identifier'
        )

    def validate(self, data):
        """
        Valide se existe outro usuário com o mesmo endereço de email
        e verifique se a senha não corresponde.
        """

        logging.info("Validando os dados para atualização do usuário na plataforma ALMA.")

        if "user" not in data.keys():
            raise ParseError(_('User object is required.'))

        return data

    def update(self, instance, validated_data):
        """
        Atualiza os dados do usuário
        """

        logging.info(f"Instancia para atualização na plataforma ALMA: {instance}")
        logging.info(f"Dados para atualização na plataforma ALMA: {validated_data}")

        user = User.objects.get(id=instance.user.id)
        updated_user = UserSerializer().update(user, validated_data['user'])
        instance.user = updated_user

        if "identifier" in validated_data.keys():
            instance.identifier = validated_data['identifier']

        if "permission" in validated_data.keys():
            instance.permission = validated_data['permission']

        if 'photo' in validated_data.keys():
            instance.photo = validated_data['photo']

        instance.save()

        logging.info("Usuário da plataforma ALMA atualizado com sucesso!")

        return instance


class AlmaUserRegisterSerializer(ModelSerializer):
    """
    O serializer para registrar um novo usuário
    """

    user = UserRegisterSerializer()

    class Meta:
        model = AlmaUser
        fields = (
            'id', 'user', 'permission', 'photo', 'created_at',
            'updated_at'
        )

    def validate(self, data):
        """
        Valide se existe outro usuário com o mesmo endereço de email
        e verifique se a senha não corresponde.
        """

        logging.info("Validando os dados para criação do usuário na plataforma ALMA.")

        if "user" not in data.keys():
            raise ParseError(_('User object is required.'))

        return data

    def create(self, validated_data):
        """
        Cria e retorna um novo usuário
        """

        logging.info(f"Dados para criação do usuário na plataforma ALMA: {validated_data}")

        serializer = UserRegisterSerializer()
        user_validated_data = serializer.validate(validated_data['user'])
        user = serializer.create(user_validated_data)

        alma_user = AlmaUser(user=user)

        if "permission" in validated_data.keys():
            alma_user.permission = validated_data['permission']

        if 'photo' in validated_data.keys():
            alma_user.photo = validated_data['photo']

        alma_user.save()

        logging.info("Usuário da plataforma ALMA criado com sucesso!")

        return alma_user