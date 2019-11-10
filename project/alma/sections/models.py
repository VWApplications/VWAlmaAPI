from django.db import models
from common.models import BaseModel
from alma.disciplines.models import Discipline
from .enum import MethodologyTypeSet


class Section(BaseModel):
    """
    seções da disciplina.
    """

    discipline = models.ForeignKey(
        Discipline,
        on_delete=models.CASCADE,
        verbose_name='Disciplina',
        related_name='sections'
    )

    title = models.CharField(
        "Título",
        max_length=100,
        help_text="Título da seção"
    )

    description = models.TextField(
        "Descrição",
        help_text="Descrição da seção"
    )

    methodology = models.CharField(
        "Tipo de metodologia",
        max_length=50,
        choices=[(item.value, item.value) for item in MethodologyTypeSet],
        help_text="Tipo de metodologia ativa de aprendizado ou tradicional.",
        default=MethodologyTypeSet.TRADITIONAL.value
    )

    is_closed = models.BooleanField(
        "Está Fechada?",
        default=True,
        help_text="Verifica se a seção da disciplina está fechada."
    )

    is_finished = models.BooleanField(
        "Foi finalizada",
        default=False,
        help_text="Verifica se a seção da disciplina foi finalizada."
    )

    def __str__(self):
        """
        Retorna o objeto em forma de string.
        """

        return '{0}'.format(self.title)

    class Meta:
        db_table = "alma_sections"
        ordering = ['title', 'created_at']