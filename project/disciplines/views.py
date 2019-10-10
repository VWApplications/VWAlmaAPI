from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from common.utils import convert_to_json
from core.views import CustomPagination
from .serializers import DisciplineSerializer
from .permissions import (
    OnlyLoggedTeacherCanCreateDiscipline,
    UpdateYourOwnDisciplines
)
from .models import Discipline
import logging


class DisciplineViewSet(ModelViewSet):
    """
    View para gerenciar disciplinas.
    """

    queryset = Discipline.objects.all()
    serializer_class = DisciplineSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        """
        Se o usuário for um estudante filtra as disciplinas que ele pertence,
        já se for um professor filtra as disciplinas criadas.
        """

        logging.info("Buscando as disciplinas")

        if (self.action == "list"):
            if self.request.user.is_teacher:
                queryset = self.filter_teacher_disciplines()
            else:
                queryset = self.filter_student_disciplines()

            logging.info(f"Queryset: {convert_to_json(queryset)}")
        else:
            queryset = Discipline.objects.all()

        return queryset

    def filter_teacher_disciplines(self):
        """
        Pega as disciplinas que o professor criou ou é monitor.
        """

        logging.info("Buscando as disciplinas do professor")

        created_disciplines = Discipline.objects.filter(
            teacher=self.request.user
        )

        logging.info(f"Disciplinas criadas: {convert_to_json(created_disciplines)}")

        monitor_disciplines = Discipline.objects.filter(
            monitors=self.request.user
        )

        logging.info(f"Disciplinas como monitor: {convert_to_json(monitor_disciplines)}")

        queryset = []
        for discipline in created_disciplines:
            queryset.append(discipline)

        for discipline in monitor_disciplines:
            queryset.append(discipline)

        filtered = self.request.query_params.get('filter', None)
        logging.info(f"Parâmetro da requisição: {filtered}")

        if filtered == 'created':
            queryset = created_disciplines
        elif filtered == 'monitor':
            queryset = monitor_disciplines

        return queryset

    def filter_student_disciplines(self):
        """
        Pega as disciplinas que o estudante pertence.
        """

        logging.info("Buscando as disciplinas do estudante.")

        student_disciplines = Discipline.objects.filter(
            students=self.request.user
        )

        logging.info(f"Disciplinas como estudante: {convert_to_json(student_disciplines)}")

        monitor_disciplines = Discipline.objects.filter(
            monitors=self.request.user
        )

        logging.info(f"Disciplinas como monitor: {convert_to_json(monitor_disciplines)}")

        queryset = []
        for discipline in student_disciplines:
            queryset.append(discipline)

        for discipline in monitor_disciplines:
            queryset.append(discipline)

        filtered = self.request.query_params.get('filter', None)
        logging.info(f"Parâmetro da requisição: {filtered}")

        if filtered == 'student':
            queryset = student_disciplines
        elif filtered == 'monitor':
            queryset = monitor_disciplines

        return queryset

    def get_permissions(self):
        """
        Instancia e retorna a lista de permissões que essa ação requer.

        Ações: list, create, destroy, retrieve, update, partial_update
        """

        logging.info(f"Action disparada: {self.action}")

        if self.action == 'list' or self.action == 'create':
            permission_classes = (OnlyLoggedTeacherCanCreateDiscipline,)
        else:
            permission_classes = (IsAuthenticated, UpdateYourOwnDisciplines,)

        logging.info(f"Permissões disparadas: {permission_classes}")

        return [permission() for permission in permission_classes]
