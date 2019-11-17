from rest_framework import serializers
from .models import Submission


class SubmissionSerializer(serializers.ModelSerializer):
    """
    Serializado de dados das submissões.
    """

    class Meta:
        model = Submission
        fields = ['id', 'section', 'answers', 'score', 'exam', 'qtd', 'grade', 'correct_answers', 'student']
        extra_kwargs = {
            "correct_answers": {"read_only": True},
            "score": {"read_only": True},
            "qtd": {"read_only": True},
            "grade": {"read_only": True}
        }

    def create(self, validated_data):
        """
        Anular criação
        """

        pass

    def update(self, instance, validated_data):
        """
        Anular atualização
        """

        pass
