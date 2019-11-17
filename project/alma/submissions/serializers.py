from rest_framework import serializers
from rest_framework.exceptions import ParseError
from alma.sections.models import Section
from alma.accounts.models import AlmaUser
from alma.questions.models import Alternative, Question
from .enum import ExamSet
from .models import Submission
import logging


class SubmissionSerializer(serializers.ModelSerializer):
    """
    Serializado de dados das submissões.
    """

    class Meta:
        model = Submission
        fields = ['id', 'section', 'answers', 'score', 'exam', 'qtd', 'grade', 'answers_test', 'student']
        extra_kwargs = {
            "section": {"required": False},
            "student": {"required": False},
            "answers_test": {"read_only": True},
            "score": {"read_only": True},
            "qtd": {"read_only": True},
            "grade": {"read_only": True}
        }

    def validate(self, data):
        """
        Valida os dados para a criação da submissão.
        """

        logging.info("Validando os dados para criação da submissão.")

        if "section" not in data.keys():
            raise ParseError("A identificação da sessão da avaliação é obrigatória.")

        if "answers" not in data.keys():
            raise ParseError("O JSON de respostas é obrigatório.")

        if "student" not in data.keys():
            raise ParseError("O identificação do estudante que submeteu as respostas é obrigatório.")

        if data['exam'] not in [item.value for item in ExamSet]:
            raise ParseError("Tipo de avaliação inexistente.")

        return data

    def calculate_score(self, answers):
        """
        Calcula a nota final.
        """

        logging.info(f"Respostas: {answers}")
        score = 0
        qtd = 0
        v_or_f = {}
        shots = {}
        multiple_choices = {}

        if "VorF" in answers.keys():
            for question in answers['VorF'].items():
                alternative_answes = {}
                for alternative in question[1].items():
                    qtd += 4
                    alternative_id = int(alternative[0].split("A")[1])
                    obj = Alternative.objects.get(id=alternative_id)
                    alternative_answes[f"A{obj.id}"] = obj.is_correct
                    if obj.is_correct == alternative[1]:
                        score += 4
                v_or_f[question[0]] = alternative_answes
        
        if "multiple_choices" in answers.keys():
            for question in answers['multiple_choices'].items():
                qtd += 4
                question_id = int(question[0].split("Q")[1])
                obj = Question.objects.get(id=question_id)
                for alternative in obj.alternatives.all():
                    if alternative.is_correct:
                        multiple_choices[f"Q{obj.id}"] = alternative.id

                    if alternative.id == int(question[1]):
                        if alternative.is_correct:
                            score += 4

        if "shots" in answers.keys():
            for question in answers['shots'].items():
                qtd += 4
                question_id = int(question[0].split("Q")[1])
                obj = Question.objects.get(id=question_id)
                correct_alternative = None
                for alternative in obj.alternatives.all():
                    if alternative.is_correct:
                        shots[f"Q{obj.id}"] = f"A{alternative.id}"
                        correct_alternative = alternative

                for alternative in question[1].items():
                    alternative_id = int(alternative[0].split("A")[1])
                    if correct_alternative.id == alternative_id:
                        score += int(alternative[1])

        grade = round((score/qtd) * 10, 2)

        answers_test = {
            "VorF": v_or_f,
            "shots": shots,
            "multiple_choices": multiple_choices

        }
        logging.info(f"Gabarito: {answers_test}")
        logging.info(f"Nota: {score}/{qtd} x 10 = {grade}")

        return score, qtd, grade, answers_test

    def create(self, validated_data):
        """
        Cria e retorna um novo usuário
        """

        logging.info(f"Dados para criação da submissão: {validated_data}")

        score, qtd, grade, answers_test = self.calculate_score(validated_data['answers'])

        submission = Submission.objects.create(
            section=validated_data['section'],
            student=validated_data['student'],
            answers=validated_data['answers'],
            exam=validated_data['exam'],
            score=score, qtd=qtd, grade=grade,
            answers_test=answers_test
        )

        logging.info("Submissão criada com sucesso!")

        return submission
