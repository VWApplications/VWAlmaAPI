from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ParseError
from rest_framework.serializers import ModelSerializer, CharField, DateTimeField, SerializerMethodField
from django.contrib.auth import get_user_model
import logging

User = get_user_model()


class UserSerializer(ModelSerializer):
    """
    O serializado para pegar os dados do usuário
    """

    short_name = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'name', 'short_name',
            'photo', 'is_teacher', 'last_login',
            'created_at', 'updated_at', 'identifier'
        )
        extra_kwargs = {'is_teacher': {'read_only': True}}

    def get_short_name(self, obj):
        """
        Pega o nome curto do usuário.
        """

        return obj.short_name

    def update(self, instance, validated_data):
        """
        Atualiza os dados do usuário
        """

        logging.info("Instancia para atualização: " + str(instance))
        logging.info("Dados para atualização: " + str(validated_data))

        if "email" in validated_data.keys():
            instance.email = validated_data['email']

        if "name" in validated_data.keys():
            instance.name = validated_data['name']

        if "identifier" in validated_data.keys():
            instance.identifier = validated_data['identifier']

        if 'photo' in validated_data.keys():
            instance.photo = validated_data['photo']

        instance.save()

        logging.info("Usuário atualizado com sucesso!")

        return instance


class UserPasswordSerializer(ModelSerializer):
    """
    O serializador para atualizar a senha do usuário.
    """

    password = CharField(write_only=True, style={'input_type': 'password'})

    new_password = CharField(write_only=True, style={'input_type': 'password'})

    confirm_password = CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('password', 'new_password', 'confirm_password')

    def update(self, instance, validated_data):
        """
        Atualiza a senha do usuário.
        """

        logging.info("Instancia para atualização: " + str(instance))

        if "password" not in validated_data.keys():
            raise ParseError(_('Old password is required.'))

        if "new_password" not in validated_data.keys():
            raise ParseError(_('New password is required.'))

        if "confirm_password" not in validated_data.keys():
            raise ParseError(_('Password confirmation is required.'))

        password = validated_data['password']
        new_password = validated_data['new_password']
        confirm_password = validated_data['confirm_password']

        # Verifique se a senha antiga está correta.
        if not instance.check_password(password):
            raise ParseError(_('Old password invalid.'))

        # Verifica se ambas as senhas coincidem.
        if new_password != confirm_password:
            raise ParseError(_('The new passwords do not match.'))

        instance.set_password(new_password)

        instance.save()

        logging.info("Senha atualizada com sucesso!")

        return instance


class UserRegisterSerializer(ModelSerializer):
    """
    O serializer para registrar um novo usuário
    """

    password = CharField(write_only=True, style={'input_type': 'password'})

    confirm_password = CharField(write_only=True, style={'input_type': 'password'})

    last_login = DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'name', 'email', 'short_name',
            'photo', 'is_teacher', 'last_login', 'created_at',
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

        logging.info("Dados para criação do usuário: " + str(validated_data))

        user = User(
            email=validated_data['email'],
            name=validated_data['name'],
            is_teacher=validated_data.get('is_teacher', False)
        )

        if 'photo' in validated_data.keys():
            user.photo = validated_data['photo']

        user.set_password(validated_data['password'])

        user.save()

        logging.info("Usuário criado com sucesso!")

        return user
