from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.db import models
from core.models import BaseModel

User = get_user_model()


class DisciplineManager(models.Manager):
    """
    Crie um conjunto de consultas personalizado da disciplina.
    """

    def available(self, user):
        """
        Remova do conjunto de consultas a disciplina que o professor é proprietário,
        alunos e monitores que estão dentro da disciplina e disciplinas fechadas.
        """

        return self.get_queryset().exclude(
            models.Q(teacher=user) |
            models.Q(students__email=user.email) |
            models.Q(monitors__email=user.email)
        )


class Discipline(BaseModel):
    """
    Classe que gerencia as disciplinas da TBL.
    """

    title = models.CharField(
        "Título",
        max_length=50,
        help_text="Título da disciplina"
    )

    institution = models.CharField(
        'Instituição',
        help_text="Universidade ou escola em que o usuário está inserido.",
        max_length=50,
        blank=True
    )

    course = models.CharField(
        "Curso",
        max_length=50,
        help_text="Curso que é ministrado a disciplina.",
        blank=True
    )

    description = models.TextField(
        "Descrição",
        help_text="Ementa da disciplina."
    )

    classroom = models.CharField(
        'Sala',
        max_length=20,
        help_text="Turma da disciplina.",
    )

    password = models.CharField(
        'Senha',
        max_length=30,
        help_text="Senha para entrar na disciplina.",
        blank=True
    )

    students_limit = models.PositiveIntegerField(
        'Limite de estudantes.',
        default=5,
        help_text="Limite de estudantes para entrar na turma.",
        validators=[
            MaxValueValidator(
                150,
                _('There can be no more than %(limit_value)s students in the class.')
            ),
            MinValueValidator(
                5,
                _('Must have at least %(limit_value)s students in class.')
            )
        ]
    )

    monitors_limit = models.PositiveIntegerField(
        "Limite de monitores",
        default=0,
        help_text="Limite de monitores para entrar na turma.",
        validators=[
            MaxValueValidator(
                15,
                _('There can be no more than %(limit_value)s monitors in the class.')
            ),
            MinValueValidator(
                0,
                _('Ensure this value is greater than or equal to %(limit_value)s.')
            )
        ]
    )

    is_closed = models.BooleanField(
        "Está fechada?",
        default=False,
        help_text="Verifica se a disciplina está fechada."
    )

    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Professor",
        related_name="disciplines"
    )

    students = models.ManyToManyField(
        User,
        verbose_name='Alunos',
        related_name='student_classes',
        blank=True
    )

    monitors = models.ManyToManyField(
        User,
        verbose_name='Monitores',
        related_name='monitor_classes',
        blank=True
    )

    # Insere o queryset na modelo.
    objects = DisciplineManager()

    def get_discipline_url(self):
        """
        Pega o nome da disciplina formatado para urls.
        """

        title = self.title.replace(" ", "-").lower()

        return '{0}-{1}'.format(self.id, title)

    def __str__(self):
        """
        Objeto em forma de string.
        """

        return self.get_discipline_url()

    class Meta:
        db_table = "disciplines"
        ordering = ['title', 'created_at']
