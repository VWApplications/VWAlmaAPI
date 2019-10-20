from django.contrib.auth import get_user_model
from django.db import models
from core.models import BaseModel

from disciplines.models import Discipline

User = get_user_model()


class Group(BaseModel):
    """
    Cria grupos da disciplina.
    """

    discipline = models.ForeignKey(
        Discipline,
        on_delete=models.CASCADE,
        verbose_name='Discipline',
        related_name='groups',
    )

    title = models.CharField(
        'Título',
        max_length=50,
        help_text="Título do grupo"
    )

    students_limit = models.PositiveIntegerField(
        "Limite de estudantes",
        default=0,
        help_text="Limite de estudantes do grupo"
    )

    is_provided = models.BooleanField(
        "Foi liberado?",
        default=False,
        help_text="O grupo foi liberado para visualização pelos estudantes."
    )

    students = models.ManyToManyField(
        User,
        verbose_name='Students',
        related_name='student_groups',
        blank=True
    )

    def __str__(self):
        """
        Retorna o objeto em formato de string.
        """

        return self.title

    class Meta:
        db_table = "groups"
        ordering = ['title', 'created_at']