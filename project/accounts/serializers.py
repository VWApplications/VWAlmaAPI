from django.contrib.auth import get_user_model
from rest_framework.exceptions import ParseError
from rest_framework.serializers import ModelSerializer, Serializer, CharField
import logging

User = get_user_model()


class UserSerializer(ModelSerializer):
    """
    O serializado para pegar os dados do usuário
    """

    class Meta:
        model = User
        fields = (
            'id', 'email', 'name', 'short_name',
            'created_at', 'updated_at',
            'created_at_formated', 'updated_at_formated'
        )

    def update(self, instance, validated_data):
        """
        Atualiza os dados do usuário
        """

        logging.info(f"Instancia para atualização: {instance}")
        logging.info(f"Dados para atualização: {validated_data}")

        if "email" in validated_data.keys():
            if validated_data['email'] != instance.email and User.objects.filter(email=validated_data['email']).exists():
                raise ParseError("Já existe um usuário com este email.")

            instance.email = validated_data['email']

        if "name" in validated_data.keys():
            instance.name = validated_data['name']

        instance.save()

        logging.info("Usuário atualizado com sucesso!")

        return instance


class UserPasswordSerializer(Serializer):
    """
    O serializador para atualizar a senha do usuário.
    """

    password = CharField(write_only=True, style={'input_type': 'password'})

    new_password = CharField(write_only=True, style={'input_type': 'password'})

    confirm_password = CharField(write_only=True, style={'input_type': 'password'})

    def update(self, instance, validated_data):
        """
        Atualiza a senha do usuário.
        """

        logging.info(f"Instancia para atualização: {instance}")

        if "password" not in validated_data.keys():
            raise ParseError("A senha antiga é obrigatória.")

        if "new_password" not in validated_data.keys():
            raise ParseError("A nova senha é obrigatória.")

        if "confirm_password" not in validated_data.keys():
            raise ParseError("A confirmação de senha é obrigatória.")

        password = validated_data['password']
        new_password = validated_data['new_password']
        confirm_password = validated_data['confirm_password']

        # Verifique se a senha antiga está correta.
        if not instance.check_password(password):
            raise ParseError("Senha antiga inválida.")

        # Verifica se ambas as senhas coincidem.
        if new_password != confirm_password:
            raise ParseError("As novas senhas não combinam.")

        instance.set_password(new_password)

        instance.save()

        logging.info("Senha atualizada com sucesso!")

        return instance


class ResetPasswordSerializer(Serializer):
    """
    Reseta e cria uma nova senha.
    """

    new_password = CharField(write_only=True, style={'input_type': 'password'})

    confirm_password = CharField(write_only=True, style={'input_type': 'password'})

    def update(self, instance, validated_data):
        """
        Atualiza a senha do usuário.
        """

        logging.info(f"Instancia para atualização: {instance}")

        reset = validated_data['reset']

        if reset.confirmed:
            raise ParseError("A chave especificada já foi utilizada.")

        if "new_password" not in validated_data.keys():
            raise ParseError("A nova senha é obrigatória.")

        if "confirm_password" not in validated_data.keys():
            raise ParseError("A confirmação da senha é obrigatória.")

        new_password = validated_data['new_password']
        confirm_password = validated_data['confirm_password']

        # Verifica se ambas as senhas coincidem.
        if new_password != confirm_password:
            raise ParseError("As novas senhas não combinam.")

        instance.set_password(new_password)
        reset.confirmed = True

        instance.save()
        reset.save()

        logging.info("Senha atualizada com sucesso!")

        return instance


class UserRegisterSerializer(ModelSerializer):
    """
    O serializer para registrar um novo usuário
    """

    password = CharField(write_only=True, style={'input_type': 'password'})

    confirm_password = CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = (
            'id', 'name', 'email', 'short_name',
            'created_at', 'updated_at', 'password',
            'confirm_password'
        )

    def validate(self, data):
        """
        Valide se existe outro usuário com o mesmo endereço de email
        e verifique se a senha não corresponde.
        """

        logging.info("Validando os dados para criação do usuário.")

        if "name" not in data.keys() or not data['name']:
            raise ParseError("O nome é obrigatório.")

        if "email" not in data.keys() or not data['email']:
            raise ParseError("O email é obrigatório.")

        if "password" not in data.keys():
            raise ParseError("A senha é obrigatória.")

        if "confirm_password" not in data.keys():
            raise ParseError("A confirmação de senha é obrigatória")

        email = data['email']
        password = data['password']
        confirm_password = data['confirm_password']

        # Verifique se existe outro usuário com o mesmo endereço de email
        user = User.objects.filter(email=email)
        if user.exists():
            raise ParseError("O usuário já foi registrado.")

        # Verifique se as senhas não coincidem.
        if password != confirm_password:
            raise ParseError("As senhas não combinam.")

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

        logging.info("Usuário criado com sucesso!")

        return user
