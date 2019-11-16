from rest_framework import serializers
from rest_framework.exceptions import ParseError
from .models import Submission
import logging


class SubmissionSerializer(serializers.ModelSerializer):
    """
    Serializado de dados das submissões.
    """

    class Meta:
        model = Submission
        fields = ('id', 'section', 'answers', 'score', 'exam', 'student')

    def validate(self, data):
        """
        Valida os dados para a criação da submissão.
        """

        logging.info("Validando os dados para criação da submissão.")

        if "section" not in data.keys():
            raise ParseError("A identificação da sessão da avaliação é obrigatória.")

        if "answers" not in data.keys():
            raise ParseError("O JSON de respostas é obrigatório.")

        if "student" not in data.keys():
            raise ParseError("O identificação do estudante que submeteu as respostas é obrigatório.")

        return data

    def create(self, validated_data):
        """
        Cria e retorna um novo usuário
        """

        logging.info(f"Dados para criação da submissão: {validated_data}")

        submission = Submission.objects.create(
            **validated_data
        )

        logging.info("Submissão criada com sucesso!")

        return submission
