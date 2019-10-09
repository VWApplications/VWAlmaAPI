from django.forms.models import model_to_dict


def convert_to_json(model, fields=None):
    """
    Transforma um objeto em um dicionário python ou uma
    lista de dicionários
    """

    if type(model) == dict:
        if not fields:
            fields = [field.name for field in model._meta.fields]

        return model_to_dict(model, fields=fields)

    result = []
    for obj in model:

        if not fields:
            fields = [field.name for field in obj._meta.fields]

        result.append(model_to_dict(obj, fields=fields))

    return result