from django.db import models
from common.models import BaseModel


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
        db_table = "alma_news"
        ordering = ('created_at', 'title')
