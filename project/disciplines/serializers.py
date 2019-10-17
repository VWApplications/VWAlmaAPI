from rest_framework.serializers import ModelSerializer, CharField
from rest_framework.exceptions import ParseError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from .models import Discipline
import logging

User = get_user_model()


class UserDisciplineSerializer(ModelSerializer):
    """
    Serializado de dados do professor da disciplina.
    """

    class Meta:
        model = User
        fields = ('id', 'short_name', 'email', 'photo', 'identifier')


class DisciplineSerializer(ModelSerializer):
    """
    Serializador para disciplinas.
    """

    teacher = UserDisciplineSerializer(read_only=True)
    students = UserDisciplineSerializer(read_only=True, many=True)
    monitors = UserDisciplineSerializer(read_only=True, many=True)

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

        teacher = self.context['request'].user.id

        return teacher

    def create(self, validated_data):
        """
        Cria e retorna uma nova disciplina
        """

        logging.info("Dados para criação da disciplina: " + str(validated_data))

        try:
            teacher = User.objects.get(id=self.current_user())
            logging.info("Professor: " + str(teacher))
        except User.DoesNotExist as error:
            logging.error(error)
            raise ParseError(_('Authenticated teacher not found.'))

        discipline = Discipline.objects.create(
            **validated_data,
            teacher=teacher
        )

        discipline.save()

        logging.info("Disciplina criada com sucesso!")

        return discipline