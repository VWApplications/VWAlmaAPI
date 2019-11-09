from rest_framework.serializers import ModelSerializer, CharField
from rest_framework.exceptions import ParseError
from alma.accounts.models import AlmaUser
from accounts.serializers import UserSerializer
from common.utils import convert_to_json
from .models import Discipline
import logging


class UserDisciplineSerializer(ModelSerializer):
    """
    Serializado de dados do professor da disciplina.
    """

    user = UserSerializer()

    class Meta:
        model = AlmaUser
        fields = ('id', 'user', 'photo', 'identifier', 'permission')


class DisciplineSerializer(ModelSerializer):
    """
    Serializador para disciplinas.
    """

    teacher = UserDisciplineSerializer(read_only=True)

    password = CharField(write_only=True, required=False)

    class Meta:
        model = Discipline
        fields = (
            'id', 'title', 'description', 'course', 'teacher',
            'classroom', 'password', 'students', 'monitors',
            'students_limit', 'monitors_limit', 'is_closed',
            'institution'
        )
        read_only_fields = ('students', 'monitors')

    def current_user(self):
        """
        Pega o usuário logado.
        """

        teacher = self.context['request'].user.alma_user.id

        return teacher

    def create(self, validated_data):
        """
        Cria e retorna uma nova disciplina
        """

        logging.info(f"Dados para criação da disciplina: {validated_data}")

        try:
            teacher = AlmaUser.objects.get(id=self.current_user())
            logging.info(f"Professor: {convert_to_json(teacher)}")
        except AlmaUser.DoesNotExist as error:
            logging.error(error)
            raise ParseError("Professor não encontrado.")

        discipline = Discipline.objects.create(
            **validated_data,
            teacher=teacher
        )

        discipline.save()

        logging.info("Disciplina criada com sucesso!")

        return discipline