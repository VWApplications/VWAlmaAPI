from django.db import models
from core.models import BaseModel
from sections.models import Section
from questions.enum import TypeSet


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

    def __str__(self):
        """
        Questão no formato string.
        """

        return self.title

    class Meta:
        db_table = "questions"
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
        db_table = "alternatives"
        ordering = ['created_at']