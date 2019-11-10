from django.db import models
from common.models import BaseModel
from alma.sections.models import Section
from .enum import TypeSet, ExamTypeSet


class Question(BaseModel):
    """
    Questões para inserir nos exercícios ou nas provas.
    """

    title = models.CharField(
        "Título",
        max_length=50,
        help_text="Título da questão"
    )

    description = models.TextField(
        "Descrição",
        help_text="Descrição da seção",
        blank=True
    )

    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name='questions'
    )

    question = models.CharField(
        "Tipo de questão",
        max_length=20,
        choices=[(item.value, item.value) for item in TypeSet],
        default=TypeSet.MULTIPLE_CHOICES.value,
        help_text="Tipos de questão que podem ser criadas."
    )

    type = models.CharField(
        "Tipo de avaliação",
        max_length=30,
        choices=[(item.value, item.value) for item in ExamTypeSet],
        help_text="Verificar o tipo de avaliação que a questão irá fazer parte.",
        default=ExamTypeSet.EXERCISE.value
    )

    def __str__(self):
        """
        Questão no formato string.
        """

        return self.title

    class Meta:
        db_table = "alma_questions"
        ordering = ['title', 'created_at']


class Alternative(BaseModel):
    """
    Alternativas da questão.
    """

    title = models.TextField(
        "Título",
        help_text="Título da alternativa",
        blank=True
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='alternatives'
    )

    is_correct = models.BooleanField(
        "É a alternativa correta?",
        default=False,
        help_text="Verifica se essa alternativa é a correta."
    )

    def __str__(self):
        """
        Objeto em formato de string
        """

        return self.title

    class Meta:
        db_table = "alma_alternatives"
        ordering = ['created_at']