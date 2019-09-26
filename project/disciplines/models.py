from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.db import models
from core.models import BaseModel

# Get the custom user from settings
User = get_user_model()


class DisciplineManager(models.Manager):
    """
    Create a custom search discipline queryset.
    """

    def available(self, user):
        """
        Remove from queryset the discipline that teacher is owner,
        students and monitors that are inside discipline and disciplines
        that are closed.
        """

        return self.get_queryset().exclude(
            models.Q(teacher=user) |
            models.Q(students__email=user.email) |
            models.Q(monitors__email=user.email)
        )


class Discipline(BaseModel):
    """
    Class that manages the disciplines part of TBL.
    """

    title = models.CharField(
        _("Title"),
        max_length=100,
        help_text=_("Title of discipline")
    )

    institution = models.CharField(
        _('Institution'),
        help_text=_("University or School in which the user is inserted."),
        max_length=100,
        blank=True
    )

    course = models.CharField(
        _("Course"),
        max_length=100,
        help_text=_("Course that is ministered the discipline"),
        blank=True
    )

    description = models.TextField(
        _("Description"),
        help_text=_("Description of discipline")
    )

    classroom = models.CharField(
        _('Classroom'),
        max_length=10,
        help_text=_("Classroom title of discipline."),
    )

    password = models.CharField(
        _('Password'),
        max_length=30,
        help_text=_("Password to get into the class."),
        blank=True
    )

    students_limit = models.PositiveIntegerField(
        _('Students limit'),
        default=0,
        help_text=_("Students limit to get in the class."),
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
        _("Monitors limit"),
        default=0,
        help_text=_("Monitors limit to insert in the class."),
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
        _("Is closed?"),
        default=False,
        help_text=_("Close discipline.")
    )

    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("Teacher"),
        related_name="disciplines"
    )

    # Class students
    students = models.ManyToManyField(
        User,
        verbose_name='Students',
        related_name='student_classes',
        blank=True
    )

    # Class monitors
    monitors = models.ManyToManyField(
        User,
        verbose_name='Monitors',
        related_name='monitor_classes',
        blank=True
    )

    # Insert new queryset into the model
    objects = DisciplineManager()

    def __str__(self):
        """
        Returns the object as a string, the attribute that will represent
        the object.
        """

        return '{0}: {1} - {2}'.format(self.course, self.title, self.classroom)

    class Meta:
        db_table = "disciplines"
        ordering = ['title', 'created_at']
