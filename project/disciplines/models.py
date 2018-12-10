from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

# Python modules
import re

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


class Discipline(models.Model):
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
        max_length=100
    )

    course = models.CharField(
        _("Course"),
        max_length=100,
        help_text=_("Course that is ministered the discipline")
    )

    description = models.TextField(
        _("Description"),
        help_text=_("Description of discipline")
    )

    classroom_validator = validators.RegexValidator(
        re.compile('^Class|^Turma [A-Z]$'),
        _("Enter a valid classroom, the classroom need to be 'Class A-Z'")
    )

    classroom = models.CharField(
        _('Classroom'),
        max_length=10,
        default="Class A",
        help_text=_("Classroom title of discipline."),
        validators=[classroom_validator]
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
                60,
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
                5,
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
        related_name="disciplines",
        related_query_name="discipline"
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

     # Create a date when the discipline is created
    created_at = models.DateTimeField(
        _('Created at'),
        help_text=_("Date that the discipline is created."),
        auto_now_add=True
    )

    # Create or update the date after the discipline is updated
    updated_at = models.DateTimeField(
        _('Updated at'),
        help_text=_("Date that the discipline is updated."),
        auto_now=True
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
        verbose_name = _("Discipline")
        verbose_name_plural = _("Disciplines")
        ordering = ['title', 'created_at']
