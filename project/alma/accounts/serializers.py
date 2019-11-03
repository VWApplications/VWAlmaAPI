from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ParseError
from rest_framework.serializers import ModelSerializer, CharField
from accounts.serializers import UserSerializer
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

    def update(self, instance, validated_data):
        """
        Atualiza os dados do usuário
        """

        logging.info(f"Instancia para atualização: {instance}")
        logging.info(f"Dados para atualização: {validated_data}")

        if "email" in validated_data.keys():
            if validated_data['email'] != instance.user.email and User.objects.filter(email=validated_data['email']).exists():
                raise ParseError(_('There is already a user with this email.'))

            instance.user.email = validated_data['email']

        if "name" in validated_data.keys():
            instance.user.name = validated_data['name']

        if "identifier" in validated_data.keys():
            instance.identifier = validated_data['identifier']

        if "permission" in validated_data.keys():
            instance.permission = validated_data['permission']

        if 'photo' in validated_data.keys():
            instance.photo = validated_data['photo']

        instance.save()
        instance.user.save()

        logging.info("Usuário da plataforma ALMA atualizado com sucesso!")

        return instance


class AlmaUserRegisterSerializer(ModelSerializer):
    """
    O serializer para registrar um novo usuário
    """

    password = CharField(write_only=True, style={'input_type': 'password'})

    confirm_password = CharField(write_only=True, style={'input_type': 'password'})

    user = UserSerializer()

    class Meta:
        model = User
        fields = (
            'id', 'user', 'permission', 'photo', 'created_at',
            'updated_at', 'password', 'confirm_password'
        )

    def validate(self, data):
        """
        Valide se existe outro usuário com o mesmo endereço de email
        e verifique se a senha não corresponde.
        """

        logging.info("Validando os dados para criação do usuário.")

        if "email" not in data.keys():
            raise ParseError(_('email is required.'))

        if "password" not in data.keys():
            raise ParseError(_('Password is required.'))

        if "confirm_password" not in data.keys():
            raise ParseError(_('Password confirmation is required.'))

        email = data['email']
        password = data['password']
        confirm_password = data['confirm_password']

        # Verifique se existe outro usuário com o mesmo endereço de email
        user = User.objects.filter(email=email)
        if user.exists():
            raise ParseError(_('This user has already registered.'))

        # Verifique se as senhas não coincidem.
        if password != confirm_password:
            raise ParseError(_('The passwords do not match.'))

        return data

    def create(self, validated_data):
        """
        Cria e retorna um novo usuário
        """

        logging.info(f"Dados para criação do usuário: {validated_data}")

        user = User(
            email=validated_data['email'],
            name=validated_data['name']
        )

        user.set_password(validated_data['password'])
        user.save()

        alma_user = AlmaUser(user=user)

        if "permission" in validated_data.keys():
            alma_user.permission = validated_data['permission']

        if 'photo' in validated_data.keys():
            alma_user.photo = validated_data['photo']

        alma_user.save()

        logging.info("Usuário da plataforma ALMA criado com sucesso!")

        return alma_user
