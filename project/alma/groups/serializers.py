from rest_framework import serializers
from alma.disciplines.serializers import UserDisciplineSerializer
from .models import Group


class GroupSerializer(serializers.ModelSerializer):
    """
    Serializado de dados dos grupos da disciplina.
    """

    students = UserDisciplineSerializer(required=False, many=True)

    class Meta:
        model = Group
        fields = ('id', 'title', 'students_limit', 'is_provided', 'discipline', 'students')
