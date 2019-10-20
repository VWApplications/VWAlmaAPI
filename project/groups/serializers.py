from rest_framework import serializers
from disciplines.serializers import UserDisciplineSerializer
from .models import Group
import logging


class GroupSerializer(serializers.ModelSerializer):
    """
    Serializado de dados dos grupos da disciplina.
    """

    class Meta:
        model = Group
        fields = ('id', 'title', 'students_limit', 'discipline', 'students')
