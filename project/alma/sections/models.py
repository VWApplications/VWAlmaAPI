from django.db import models
from common.models import BaseModel
from alma.disciplines.models import Discipline


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