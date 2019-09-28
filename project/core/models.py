from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    """
    Atributos básico de todas as modelos.
    """

    created_at = models.DateTimeField(
        'Criado em',
        help_text="Data na qual o objeto foi criado.",
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        'Atualizado em',
        help_text="Data na qual o objeto foi atualizado.",
        auto_now=True
    )

    def format_datetime(self, datetime, date_format="%d/%m/%Y %H:%M:%S"):
        """
        Pega a data formatada.
        """

        local_datetime = timezone.localtime(datetime)

        return local_datetime.strftime(date_format)

    class Meta:
        abstract = True


class Tag(BaseModel):
    """
    Modelo de labels
    """

    title = models.CharField('Tag', max_length=20)

    def __str__(self):
        """
        Objeto no formato string.
        """

        return self.title

    class Meta:
        db_table = "tags"


class News(BaseModel):
    """
    Modelo de notícias sobre o software.
    """

    title = models.CharField(
        'Título',
        help_text="Título da notícia",
        max_length=100
    )

    image = models.ImageField(
        upload_to='news',
        help_text='Imagem da notícia.',
        blank=True,
        null=True
    )

    link = models.URLField(
        'Link da notícia',
        blank=True,
        null=True
    )

    description = models.TextField('Descrição')

    tags = models.ManyToManyField(
        Tag,
        related_name='news',
        blank=True
    )

    def __str__(self):
        """
        Objeto no formato string.
        """

        return self.title

    class Meta:
        db_table = "news"
        ordering = ('created_at', 'title')
