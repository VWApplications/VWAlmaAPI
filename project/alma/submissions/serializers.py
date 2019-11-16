from rest_framework import serializers
from .models import Submission


class SubmissionSerializer(serializers.ModelSerializer):
    """
    Serializado de dados das submissões.
    """

    class Meta:
        model = Submission
        fields = ('id', 'section', 'answers', 'score', 'exam', 'student')
