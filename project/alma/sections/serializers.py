from rest_framework import serializers
from .models import Section


class SectionSerializer(serializers.ModelSerializer):
    """
    Serializado de dados dos grupos da disciplina.
    """

    class Meta:
        model = Section
        fields = ('id', 'title', 'description', 'is_closed', 'discipline', 'methodology', 'is_finished')
