from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.decorators import action
from rest_framework.views import status
from common.utils import convert_to_json
from common.generic_view import GenericViewSet
from common import permissions
from alma.sections.models import Section
from alma.accounts.models import AlmaUser
from alma.questions.models import Question, Alternative
from alma.accounts.enum import AlmaPermissionSet
from . import serializers
from .tasks import calculate_score
from .enum import ExamSet
from .models import Submission
import logging


class SubmissionViewSet(GenericViewSet):
    """
    View para gerenciar submissões.
    """

    serializer_class = serializers.SubmissionSerializer

    def get_permissions(self):
        """
        Instancia e retorna a lista de permissões que essa ação requer.
        """

        self.change_action()

        logging.info(f"###### Action disparada: {self.action} ######")

        if self.action == 'list' or self.action == 'retrieve' or self.action == 'destroy':
            permission_classes = (IsAuthenticated, permissions.OnlyAdmin)
        elif self.action == 'send_submission' or self.action == 'see_results':
            permission_classes = (IsAuthenticated,)
        else:
            permission_classes = (IsAuthenticated, permissions.CanNotBeDone)

        logging.info(f"Permissões disparadas: {permission_classes}")

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Pega a lista de submissões (futuramente inserir filtros)
        """

        logging.info("Pegando todas as seções.")
        return Submission.objects.all()

    @action(detail=False, methods=['post'], url_path="send", url_name="send")
    def send_submission(self, request):
        """
        Envia e cria a submissão da avaliação.
        """

        logging.info(f"Dados para criação da submissão: {request.data}")

        if "section" not in request.data.keys():
            raise ParseError("A identificação da sessão da avaliação é obrigatória.")

        if "answers" not in request.data.keys():
            raise ParseError("O JSON de respostas é obrigatório.")

        if "student" not in request.data.keys():
            raise ParseError("O identificação do estudante que submeteu as respostas é obrigatório.")

        if request.data['exam'] not in [item.value for item in ExamSet]:
            raise ParseError("Tipo de avaliação inexistente.")

        if not Section.objects.filter(id=request.data['section']).exists():
            raise ParseError("Sessão não encontrada.")

        if not AlmaUser.objects.filter(id=request.data['student'], permission=AlmaPermissionSet.STUDENT.value).exists():
            raise ParseError("Estudante não encontrado.")

        calculate_score(request.data)

        return Response({"success": True}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path="results", url_name="results")
    def see_results(self, request, pk):
        """
        Verificar o resultado da submissão.
        """

        try:
            section = Section.objects.get(id=pk)
        except Section.DoesNotExist:
            return Response({"success": False, "detail": "Seção não encontrada."}, status=status.HTTP_400_BAD_REQUEST)

        submission = Submission.objects.filter(section=section, student=request.user.alma_user, exam=section.methodology).last()
        if not submission:
            return Response({"success": False, "detail": "Submissão não encontrada."}, status=status.HTTP_400_BAD_REQUEST)

        logging.info(f"Seção: {convert_to_json(section)}")
        logging.info(f"Submissão: {convert_to_json(submission)}")

        answers = submission.answers

        result = {
            "questions": [],
            "grade": submission.grade,
            "score": submission.score,
            "qtd": submission.qtd
        }

        answer = {}
        if "VorF" in answers.keys():
            for question in answers['VorF'].items():
                answer['question'] = Question.objects.get(id=int(question[0].replace("Q", ""))).title
                answer['alternatives'] = []
                answer['correct_answer'] = []
                answer['score'] = 0
                for alternative in question[1].items():
                    alternative_obj = Alternative.objects.get(id=int(alternative[0].replace("A", "")))
                    answer['alternatives'].append({
                        "title": alternative_obj.title,
                        "answer": "V" if alternative[1] else "F"
                    })
                    answer['correct_answer'].append({
                        "title": alternative_obj.title,
                        "answer": "V" if alternative_obj.is_correct else "F"
                    })
                    if alternative_obj.is_correct == alternative[1]:
                        answer['score'] += 4

                result['questions'].append(answer)

        answer = {}
        if "multiple_choices" in answers.keys():
            for question in answers['multiple_choices'].items():
                question_obj = Question.objects.get(id=int(question[0].replace("Q", "")))
                answer['question'] = question_obj.title
                answer['alternatives'] = []
                answer['score'] = 0
                for alternative in question_obj.alternatives.all():
                    answer['alternatives'].append({
                        "title": alternative.title,
                        "answer": True if alternative.id == int(question[1]) else False
                    })

                    if alternative.is_correct:
                        answer['correct_answer'] = alternative.title

                    if alternative.id == int(question[1]):
                        if alternative.is_correct:
                            answer['score'] += 4

                result['questions'].append(answer)

        answer = {}
        if "shots" in answers.keys():
            for question in answers['shots'].items():
                question_obj = Question.objects.get(id=int(question[0].replace("Q", "")))
                answer['question'] = question_obj.title
                answer['alternatives'] = []
                answer['score'] = 0
                for alternative in question_obj.alternatives.all():
                    if alternative.is_correct:
                        answer['correct_answer'] = alternative.title
                        correct_alternative = alternative

                for alternative in question[1].items():
                    alternative_obj = Alternative.objects.get(id=int(alternative[0].replace("A", "")))
                    if correct_alternative.id == alternative_obj.id:
                        answer['score'] += int(alternative[1])

                    answer['alternatives'].append({
                        "title": alternative_obj.title,
                        "answer": int(alternative[1])
                    })

                result['questions'].append(answer)

        return Response(result, status=status.HTTP_200_OK)