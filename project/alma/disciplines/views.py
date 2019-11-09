from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import status
from common.utils import convert_to_json
from common.generic_view import CustomPagination
from alma.accounts.enum import AlmaPermissionSet
from alma.accounts.models import AlmaUser
from .permissions import (
    OnlyLoggedTeacherCanCreateDiscipline, EnterDiscipline,
    UpdateYourOwnDisciplines, SearchDiscipline, SeeDiscipline
)
from . import serializers
from .models import Discipline
import logging


class DisciplineViewSet(ModelViewSet):
    """
    View para gerenciar disciplinas.
    """

    pagination_class = CustomPagination

    def get_serializer_class(self):
        """
        Retorna a classe de serialização de acordo com o tipo
        de ação disparado.

        ações: list, create, destroy, retrieve, update, partial_update
        """

        if self.action == 'enter_discipline':
            logging.info("Entrando no EnterDisciplineSerializer.")
            return serializers.EnterDisciplineSerializer

        if self.action == 'discipline_students':
            logging.info("Entrando no UserDisciplineSerializer.")
            return serializers.UserDisciplineSerializer

        logging.info("Entrando no DisciplineSerializer.")
        return serializers.DisciplineSerializer

    def get_permissions(self):
        """
        Instancia e retorna a lista de permissões que essa ação requer.
        """

        logging.info(f"###### Action disparada: {self.action} ######")

        if self.action == 'list' or self.action == 'create':
            permission_classes = (OnlyLoggedTeacherCanCreateDiscipline,)
        elif self.action == 'retrieve' or self.action == 'discipline_students':
            permission_classes = (IsAuthenticated, SeeDiscipline)
        elif self.action == 'search_discipline':
            permission_classes = (IsAuthenticated, SearchDiscipline)
        elif self.action == 'enter_discipline':
            permission_classes = (IsAuthenticated, EnterDiscipline)
        else:
            permission_classes = (IsAuthenticated, UpdateYourOwnDisciplines)

        logging.info(f"Permissões disparadas: {permission_classes}")

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Se o usuário for um estudante filtra as disciplinas que ele pertence,
        já se for um professor filtra as disciplinas criadas.
        """

        logging.info("Buscando as disciplinas")

        if self.action == "list":
            if self.request.user.alma_user.permission == AlmaPermissionSet.TEACHER.value:
                queryset = self.filter_teacher_disciplines()
            else:
                queryset = self.filter_student_disciplines()

        elif self.action == "search_discipline":
            queryset = Discipline.objects.available(self.request.user.alma_user)
        else:
            queryset = Discipline.objects.all()

        return queryset

    def filter_teacher_disciplines(self):
        """
        Pega as disciplinas que o professor criou ou é monitor.
        """

        logging.info("Buscando as disciplinas do professor")

        created_disciplines = Discipline.objects.filter(
            teacher=self.request.user.alma_user
        )

        logging.info(f"Disciplinas criadas: {convert_to_json(created_disciplines)}")

        return created_disciplines

    def filter_student_disciplines(self):
        """
        Pega as disciplinas que o estudante pertence.
        """

        logging.info("Buscando as disciplinas do estudante.")

        student_disciplines = Discipline.objects.filter(
            students=self.request.user.alma_user
        )

        logging.info(f"Disciplinas como estudante: {convert_to_json(student_disciplines)}")

        monitor_disciplines = Discipline.objects.filter(
            monitors=self.request.user.alma_user
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

    @action(detail=False, methods=['get'], url_path="search", url_name="search")
    def search_discipline(self, request):
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
                disciplines = disciplines.order_by('teacher__user__name')

        if searched:
            disciplines = disciplines.filter(
                Q(title__icontains=searched) |
                Q(course__icontains=searched) |
                Q(classroom__icontains=searched) |
                Q(institution__icontains=searched) |
                Q(teacher__user__name__icontains=searched)
            )

        logging.info(f"Disciplinas filtradas: {disciplines}")

        page = self.paginate_queryset(disciplines)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['post'], url_path="enter", url_name="enter")
    def enter_discipline(self, request, pk):
        """
        Entra na disciplina.
        """

        logging.info("Entrando na disciplina.")

        logging.info(f"Payload: pk={pk}, data={request.data} e student={request.user.alma_user}")
        password = request.data['password']

        discipline = self.get_object()
        logging.info(f"Disciplina: {convert_to_json(discipline)}")
        logging.info(f"Lista de estudantes: {convert_to_json(discipline.students.all())}")

        if password == discipline.password:
            if discipline.students_limit <= discipline.students.count():
                return Response({"success": False, "detail": "A disciplina está lotada."}, status=status.HTTP_400_BAD_REQUEST)

            if discipline.is_closed:
                return Response({"success": False, "detail": "A disciplina está fechada."}, status=status.HTTP_400_BAD_REQUEST)

            discipline.students.add(request.user.alma_user)
            logging.info(f"Lista de estudantes atualizada: {convert_to_json(discipline.students.all())}")
        else:
            logging.warn("Senha incorreta.")
            return Response({"success": False, "detail": "Senha incorreta."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"success": True}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path="toogle_status", url_name="toogle-status")
    def toogle_discipline_status(self, request, pk):
        """
        Fechar a disciplina se tiver aberta e abre se tiver fechada.
        """

        logging.info("Alternando status da disciplina.")

        discipline = self.get_object()
        logging.info(f"Disciplina: {convert_to_json(discipline)}")
        logging.info(f"Discipline IS_CLOSED: {discipline.is_closed}")

        discipline.is_closed = not discipline.is_closed
        discipline.save()

        logging.info(f"Discipline IS_CLOSED: {discipline.is_closed}")

        return Response({"success": True}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path="reset", url_name="reset")
    def reset_discipline(self, request, pk):
        """
        Reseta a disciplina para um novo semestre.
        Deletar:
            - Groups
            - FinalGrades
            - Notification
            - Submissions
            - SessionGrades

        Modificar atributos:
            - session.is_closed = True
            - session.is_finished = True
        """

        logging.info("Resetando a disciplina.")

        discipline = self.get_object()
        logging.info(f"Disciplina: {convert_to_json(discipline)}")

        # Modificando os atributos da disciplina
        discipline.is_closed = True

        # TODO: Deletando instâncias

        # Removendo estudantes e monitores
        for student in discipline.students.all():
            discipline.students.remove(student)

        for monitor in discipline.monitors.all():
            discipline.monitors.remove(monitor)

        # TODO: Modificando os atributos das sessões

        # TODO: Deletando instâncias relacionadas as sessões

        # TODO: Deletando instâncias relacionadas as disciplinas.

        discipline.save()
        logging.info(f"Disciplina Resetada: {convert_to_json(discipline)}")

        return Response({"success": True}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path="students", url_name="students")
    def discipline_students(self, request, pk):
        """
        Pega a lista de estudantes e monitores da disciplina
        e filtra caso precise.
        """

        logging.info("Buscando os estudantes e monitores de uma disciplina.")

        discipline = self.get_object()
        logging.info(f"Disciplina: {convert_to_json(discipline)}")

        students = discipline.students.all()
        monitors = discipline.monitors.all()
        queryset = students | monitors

        filtered = self.request.query_params.get('filter', None)
        logging.info(f"Parâmetro da requisição: {filtered}")

        if filtered == "students":
            logging.info("Pegando os estudantes")
            queryset = students
        elif filtered == "monitors":
            logging.info("Pegando os monitores")
            queryset = monitors

        logging.info(f"Queryset: {queryset}")

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['post'], url_path="add_student", url_name="add-student")
    def add_student(self, request, pk):
        """
        Insere um usuário como estudante da disciplina.
        """

        logging.info("Adicionando um novo estudante a disciplina.")

        discipline = self.get_object()
        logging.info(f"Disciplina: {convert_to_json(discipline)}")

        data = request.data
        logging.info(f"Payload: {data}")

        if "email" not in data.keys():
            return Response({"success": False, "detail": "Dados de entrada incorretos."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student = AlmaUser.objects.get(user__email=data['email'])
        except AlmaUser.DoesNotExist:
            return Response({"success": False, "detail": "Usuário não encontrado."}, status=status.HTTP_400_BAD_REQUEST)

        if student in discipline.students.all():
            return Response({"success": False, "detail": "Usuário já está na disciplina."}, status=status.HTTP_400_BAD_REQUEST)

        if discipline.students_limit <= discipline.students.count():
            return Response({"success": False, "detail": "A disciplina está cheia"}, status=status.HTTP_400_BAD_REQUEST)

        discipline.students.add(student)

        return Response({"success": True}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path="remove_student", url_name="remove-student")
    def remove_student(self, request, pk):
        """
        Remove um estudante da disciplina.
        """

        logging.info("Removendo o estudante da disciplina.")

        discipline = self.get_object()
        logging.info(f"Disciplina: {convert_to_json(discipline)}")

        data = request.data
        logging.info(f"Payload: {data}")

        if "id" not in data.keys():
            return Response({"success": False, "detail": "Dados de entrada incorretos."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student = AlmaUser.objects.get(id=data['id'])
        except AlmaUser.DoesNotExist:
            return Response({"success": False, "detail": "Usuário não encontrado."}, status=status.HTTP_400_BAD_REQUEST)

        if student not in discipline.students.all() and student not in discipline.monitors.all():
            return Response({"success": False, "detail": "Estudante não pertence a disciplina."}, status=status.HTTP_400_BAD_REQUEST)

        if student in discipline.students.all():
            discipline.students.remove(student)
            for group in discipline.groups.all():
                if student in group.students.all():
                    group.students.remove(student)
        else:
            discipline.monitors.remove(student)

        return Response({"success": True}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path="toogle_student_status", url_name="toogle-student-status")
    def toogle_student_status(self, request, pk):
        """
        Transforma um estudante em monitor e vise-versa.
        """

        logging.info("Alterando status do estudante.")

        discipline = self.get_object()
        logging.info(f"Disciplina: {convert_to_json(discipline)}")

        data = request.data
        logging.info(f"Payload: {data}")

        if "id" not in data.keys():
            return Response({"success": False, "detail": "Dados de entrada invalidos."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student = AlmaUser.objects.get(id=data['id'])
        except AlmaUser.DoesNotExist:
            return Response({"success": False, "detail": "Usuário não encontrado."}, status=status.HTTP_400_BAD_REQUEST)

        if student not in discipline.students.all() and student not in discipline.monitors.all():
            return Response({"success": False, "detail": "Estudante não pertence a disciplina."}, status=status.HTTP_400_BAD_REQUEST)

        if student in discipline.students.all():
            if discipline.monitors_limit <= discipline.monitors.count():
                return Response({"success": False, "detail": "Já completou o limite de monitores"}, status=status.HTTP_400_BAD_REQUEST)

            discipline.students.remove(student)
            discipline.monitors.add(student)
        else:
            if discipline.students_limit <= discipline.students.count():
                return Response({"success": False, "detail": "A disciplina está lotada."}, status=status.HTTP_400_BAD_REQUEST)

            discipline.monitors.remove(student)
            discipline.students.add(student)

        return Response({"success": True}, status=status.HTTP_200_OK)
