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
