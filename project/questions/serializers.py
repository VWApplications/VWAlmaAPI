from rest_framework import serializers
from .models import Question


class QuestionSerializer(serializers.ModelSerializer):
    """
    Serializado de dados dos grupos da disciplina.
    """

    class Meta:
        model = Question
        fields = (
            'id', 'title', 'description', 'section', 'is_exercise', 'question_type',
            'correct_answer', 'alternative_A', 'alternative_B', 'alternative_C',
            'alternative_D'
        )
