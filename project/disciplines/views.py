from django.utils.translation import ugettext_lazy as _
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import status
from common.utils import convert_to_json
from accounts.enum import PermissionSet
from core.views import CustomPagination
from . import serializers
from . import permissions
from .models import Discipline
from django.db.models import Q
import logging


class DisciplineViewSet(ModelViewSet):
    """
    View para gerenciar disciplinas.
    """

    queryset = Discipline.objects.all()
    pagination_class = CustomPagination

    def get_queryset(self):
        """
        Se o usuário for um estudante filtra as disciplinas que ele pertence,
        já se for um professor filtra as disciplinas criadas.
        """

        logging.info("Buscando as disciplinas")

        if (self.action == "list"):
            if self.request.user.permission == PermissionSet.TEACHER.value:
                queryset = self.filter_teacher_disciplines()
            else:
                queryset = self.filter_student_disciplines()

            logging.info(f"Queryset: {convert_to_json(queryset)}")
        else:
            queryset = Discipline.objects.available(self.request.user)

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

        return created_disciplines

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

    def get_serializer_class(self):
        """
        Retorna a classe de serialização de acordo com o tipo
        de ação disparado.

        ações: list, create, destroy, retrieve, update, partial_update
        """

        logging.info(f"Action disparada: {self.action}")

        if self.action == 'enter_discipline':
            logging.info("Entrando no EnterDisciplineSerializer.")
            return serializers.EnterDisciplineSerializer

        logging.info("Entrando no DisciplineSerializer.")
        return serializers.DisciplineSerializer

    def get_permissions(self):
        """
        Instancia e retorna a lista de permissões que essa ação requer.

        Ações: list, create, destroy, retrieve, update, partial_update
        """

        logging.info(f"Action disparada: {self.action}")

        if self.action == 'list' or self.action == 'create':
            permission_classes = (permissions.OnlyLoggedTeacherCanCreateDiscipline,)
        elif self.action == 'search':
            permission_classes = (permissions.SearchDiscipline,)
        elif self.action == 'enter_discipline':
            permission_classes = (permissions.EnterDiscipline,)
        else:
            permission_classes = (IsAuthenticated, permissions.UpdateYourOwnDisciplines,)

        logging.info(f"Permissões disparadas: {permission_classes}")

        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'], url_path="search", url_name="search")
    def search(self, request):
        """
        Pega as disciplinas pesquisadas.
        """

        logging.info("Pesquisando disciplinas")

        disciplines = self.get_queryset()

        ordered = self.request.query_params.get('order', None)
        searched = self.request.query_params.get('search', None)

        logging.info(f"Parâmetros: {ordered} e {searched}")

        if ordered:
            if ordered == "course":
                disciplines = disciplines.order_by('course')
            elif ordered == "discipline":
                disciplines = disciplines.order_by('title')
            elif ordered == "teacher":
                disciplines = disciplines.order_by('teacher__name')

        if searched:
            disciplines = disciplines.filter(
                Q(title__icontains=searched) |
                Q(course__icontains=searched) |
                Q(classroom__icontains=searched) |
                Q(institution__icontains=searched) |
                Q(teacher__name__icontains=searched)
            )

        logging.info(f"Disciplinas filtradas: {disciplines}")

        page = self.paginate_queryset(disciplines)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(disciplines, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path="enter", url_name="enter")
    def enter_discipline(self, request, pk):
        """
        Entra na disciplina.
        """

        logging.info("Entrando na disciplina.")

        logging.info(f"Payload: pk={pk}, data={request.data} e student={request.user}")
        password = request.data['password']

        discipline = self.get_object()
        logging.info(f"Disciplina: {convert_to_json(discipline)}")
        logging.info(f"Lista de estudantes: {convert_to_json(discipline.students.all())}")

        if password == discipline.password:
            discipline.students.add(request.user)
            logging.info(f"Lista de estudantes atualizada: {convert_to_json(discipline.students.all())}")
        else:
            logging.warn("Senha incorreta.")
            return Response({"success": False, "detail": _("Incorrect Password.")}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"success": True}, status=status.HTTP_200_OK)