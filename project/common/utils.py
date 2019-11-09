from django.forms.models import model_to_dict
from django.db.models.query import QuerySet
from django.utils import timezone


def convert_to_json(model, fields=None):
    """
    Transforma um objeto em um dicionário python ou uma
    lista de dicionários
    """

    if isinstance(model, QuerySet) or isinstance(model, list):
        result = []
        for obj in model:

            if not fields:
                fields = [field.name for field in obj._meta.fields]

            result.append(model_to_dict(obj, fields=fields))

        return result

    if not fields:
        fields = [field.name for field in model._meta.fields]

    return model_to_dict(model, fields=fields)


def format_date(date):
    """
    Converte uma data para string.
    """

    months = {
        "January": "Janeiro",
        "February": "Fevereiro",
        "March": "Março",
        "April": "Abril",
        "May": "Maio",
        "June": "Junho",
        "July": "Julho",
        "August": "Agosto",
        "September": "Setembro",
        "October": "Outubro",
        "November": "Novembro",
        "December": "Dezembro"
    }

    local_datetime = timezone.localtime(date)

    month = date.strftime("%B")

    formated_date = date.strftime(f"%d de {months[month]} de %Y às %H:%M")

    return formated_date
