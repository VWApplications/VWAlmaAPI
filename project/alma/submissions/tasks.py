from alma.questions.models import Alternative, Question
from alma.submissions.models import Submission
from alma.sections.models import Section
from alma.accounts.models import AlmaUser
from common.utils import convert_to_json
from vwa.celery import app
import logging


@app.task(bind=True, max_retries=3)
def calculate_score(self, validated_data):
    """
    Cálcula a nota e a pontuação da avaliação de forma assincrona.
    """

    answers = validated_data['answers']

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

    grade = round((score / qtd) * 10, 2)

    correct_answers = {
        "VorF": v_or_f,
        "shots": shots,
        "multiple_choices": multiple_choices

    }
    logging.info(f"Gabarito: {correct_answers}")
    logging.info(f"Nota: {score}/{qtd} x 10 = {grade}")

    section = Section.objects.get(id=validated_data['section'])
    logging.info(f"Sessão: {convert_to_json(section)}")
    student = AlmaUser.objects.get(id=validated_data['student'])
    logging.info(f"Estudante: {convert_to_json(student)}")

    Submission.objects.create(
        section=section, student=student,
        answers=answers, exam=validated_data['exam'],
        score=score, qtd=qtd, grade=grade,
        correct_answers=correct_answers
    )

    logging.info("Submissão criada com sucesso!")
