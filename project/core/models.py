from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from datetime import datetime

class BaseModel(models.Model):
    """
    Atributos básico de todas as modelos.
    """

    # Create a date when the discipline is created
    created_at = models.DateTimeField(
        _('Created at'),
        help_text=_("Date that the object is created."),
        auto_now_add=True
    )

    # Create or update the date after the discipline is updated
    updated_at = models.DateTimeField(
        _('Updated at'),
        help_text=_("Date that the object is updated."),
        auto_now=True
    )

    def format_datetime(self, datetime, date_format="%d/%m/%Y %H:%M:%S"):
        """
        Get created at attribute formated
        """

        local_datetime = timezone.localtime(datetime)

        return local_datetime.strftime(date_format)

    class Meta:
        abstract = True


class Tag(BaseModel):
    """
    Tags for improve system functionalities.
    """

    title = models.CharField(_('Tag'), max_length=20)

    def __str__(self):
        """
        String format of object.
        """

        return self.title

    class Meta:
        db_table = "tags"


class News(BaseModel):
    """
    Informations about the software.
    """

    title = models.CharField(
        _('Title'),
        help_text=_("Title of information."),
        max_length=100
    )

    image = models.ImageField(
        upload_to='news',
        help_text=_('Image about information.'),
        verbose_name=_('Image'),
        blank=True,
        null=True
    )

    link = models.URLField(
        _('Link of information'),
        blank=True,
        null=True
    )

    description = models.TextField(_('Description'))

    tags = models.ManyToManyField(
        Tag,
        related_name='news',
        blank=True
    )

    def __str__(self):
        """
        String format of object.
        """

        return self.title

    class Meta:
        db_table = "news"
        ordering = ('created_at', 'title')
