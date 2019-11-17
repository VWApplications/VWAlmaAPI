from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.views import status
from common.generic_view import GenericViewSet, QuestionPagination
from alma.core import permissions
from common.utils import convert_to_json
from . import serializers
from .enum import TypeSet, ExamTypeSet
from .models import Question, Alternative
import logging


class QuestionViewSet(GenericViewSet):
    """
    View para gerenciar questões.
    """

    serializer_class = serializers.QuestionSerializer
    pagination_class = QuestionPagination

    def get_permissions(self):
        """
        Instancia e retorna a lista de permissões que essa ação requer.
        """

        self.change_action()

        logging.info(f"###### Action disparada: {self.action} ######")

        if self.action == 'list':
            permission_classes = (IsAuthenticated, permissions.SeePage)
        elif self.action == 'retrieve':
            permission_classes = (IsAuthenticated, permissions.SeeObjPage)
        elif self.action == 'create':
            permission_classes = (IsAuthenticated, permissions.CreateSomethingInYourOwnDisciplines)
        else:
            permission_classes = (IsAuthenticated, permissions.UpdateYourOwnDisciplines)

        logging.info(f"Permissões disparadas: {permission_classes}")

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Pega a lista de os grupos de uma determinada disciplina.
        """

        section = self.get_section()

        if section:
            if self.request.data.get('test', False):
                logging.info("Pegando as questões da prova da seção.")
                return Question.objects.filter(
                    section=section,
                    type__in=[item.value for item in ExamTypeSet if item.value != ExamTypeSet.EXERCISE.value]
                )
            else:
                logging.info("Pegando as questões da lista de exercício da seção.")
                return Question.objects.filter(section=section, type=ExamTypeSet.EXERCISE.value)

        logging.info("Pegando todas as questões.")
        return Question.objects.all()

    def validate_is_correct(self, data, question, alternative):
        """
        Valida a atualização do campo is_correct.
        """

        if data['is_correct'] is True and question.question != TypeSet.V_OR_F.value:
            question.alternatives.filter(is_correct=True).update(is_correct=False)
            alternative.is_correct = True
        else:
            alternative.is_correct = data['is_correct']

        alternative.save()

    def update_alternatives(self, alternatives, question):
        """
        Atualiza as alternativas passadas.
        """

        alternative_ids = [alternative.id for alternative in question.alternatives.all()]
        data_ids = [data['id'] for data in alternatives if "id" in data.keys()]

        counter = 0
        for data in alternatives:
            if data['is_correct'] is True:
                counter += 1

        if question.question != TypeSet.V_OR_F.value and counter != 1:
            raise ParseError("Você deve entrar com uma alternativa correta.")

        for alternative in question.alternatives.all():
            if alternative.id not in data_ids:
                alternative.delete()

        for data in alternatives:
            if data.get('id', '') in alternative_ids:
                alternative = question.alternatives.get(id=data['id'])
                alternative.title = data['title']

                self.validate_is_correct(data, question, alternative)
                alternative.save()
            else:
                alternative = Alternative.objects.create(title=data['title'], question=question)
                self.validate_is_correct(data, question, alternative)
                question.alternatives.add(alternative)

    def update(self, request, *args, **kwargs):
        """
        Atualizando os dados da questão.
        """

        question = self.get_object()

        logging.info(f"Atualizando a questão {convert_to_json(question)}")

        logging.info(f"Dados de atualização: {request.data}")
        data = request.data

        if "title" in data.keys():
            question.title = data['title']

        if "description" in data.keys():
            question.description = data['description']

        if "question" in data.keys():
            question.question = data['question']

        if "type" in data.keys():
            question.type = data['type']

        if "alternatives" in data.keys():
            alternatives = data.get('alternatives', [])
            self.update_alternatives(alternatives, question)

        question.save()

        logging.info("Questão atualizada com sucesso!")

        return Response({"success": True}, status=status.HTTP_200_OK)
