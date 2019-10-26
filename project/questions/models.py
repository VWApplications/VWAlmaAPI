from django.db import models
from core.models import BaseModel
from sections.models import Section
from questions.enum import TypeSet, CorrectAnswerSet


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
        help_text="Descrição da seção"
    )

    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name='questions'
    )

    is_exercise = models.BooleanField(
        "É um exercício?",
        default=True,
        help_text="Verifica se a questão criada é um exercício."
    )

    question_type = models.CharField(
        "Tipo de questão",
        max_length=20,
        choices=[(item.value, item.value) for item in TypeSet],
        default=TypeSet.MULTIPLE_CHOICES.value,
        help_text="Tipos de questão que podem ser criadas."
    )

    correct_answer = models.CharField(
        "Resposta correta",
        max_length=20,
        choices=[(item.value, item.value) for item in CorrectAnswerSet],
        default=CorrectAnswerSet.UNDEFINED.value,
        help_text="Respostas corretas para cada tipo de questão criada."
    )

    alternative_A = models.CharField(
        "Alternativa A",
        max_length=500,
        help_text="Descrição da alternativa A",
        blank=True
    )

    alternative_B = models.CharField(
        "Alternativa B",
        max_length=500,
        help_text="Descrição da alternativa B",
        blank=True
    )

    alternative_C = models.CharField(
        "Alternativa C",
        max_length=500,
        help_text="Descrição da alternativa C",
        blank=True
    )

    alternative_D = models.CharField(
        "Alternativa D",
        max_length=500,
        help_text="Descrição da alternativa D",
        blank=True
    )

    def __str__(self):
        """
        Questão no formato string.
        """

        return self.title

    class Meta:
        ordering = ['title', 'created_at']