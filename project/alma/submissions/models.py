from django.contrib.postgres.fields import JSONField
from django.db import models
from common.models import BaseModel
from alma.sections.models import Section
from alma.accounts.models import AlmaUser
from .enum import ExamSet

class Submission(BaseModel):
    """
    Submissão generica.
    """

    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        verbose_name='Submissão',
        related_name='submissions'
    )

    answers = JSONField("Respostas do estudante.")
    answers_test = JSONField("Gabarito da avaliação.")

    score = models.PositiveIntegerField(
        "Pontuação",
        default=0,
        help_text="Pontuação da avaliação"
    )

    qtd = models.PositiveIntegerField(
        "Quantidade total",
        default=0,
        help_text="Quantidade total de pontos"
    )

    grade = models.PositiveIntegerField(
        "Nota",
        default=0,
        help_text="Nota final"
    )

    exam = models.CharField(
        "Tipo de avaliação",
        max_length=50,
        choices=[(item.value, item.value) for item in ExamSet],
        help_text="Tipo de avalição ativa que pertence a submissão.",
        default=ExamSet.EXERCISE.value
    )

    student = models.ForeignKey(
        AlmaUser,
        on_delete=models.CASCADE,
        verbose_name="Estudante",
        related_name="submissions"
    )

    def __str__(self):
        """
        Retorna o objeto em forma de string.
        """

        return f"{self.student} - {self.exam}"

    class Meta:
        db_table = "alma_submissions"
        ordering = ['created_at']