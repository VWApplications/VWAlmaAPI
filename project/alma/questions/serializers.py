from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ParseError
from rest_framework import serializers
from common.utils import convert_to_json
from .models import Question, Alternative
import logging


class AlternativeSerializer(serializers.ModelSerializer):
    """
    Serializando os dados das alternativas.
    """

    class Meta:
        model = Alternative
        fields = ('id', 'title', 'is_correct')


class QuestionSerializer(serializers.ModelSerializer):
    """
    Serializado de dados dos grupos da disciplina.
    """

    alternatives = AlternativeSerializer(required=True, many=True)

    class Meta:
        model = Question
        fields = (
            'id', 'title', 'description', 'section', 'is_exercise', 'question_type',
            'alternatives'
        )

    def validate_creation(self, data):
        """
        Valida se somente uma alternativa está como True.
        """

        logging.info("Validando os dados para criação da questão.")

        if "alternatives" not in data.keys():
            raise ParseError(_('Field alternatives is required.'))

        if not data['alternatives']:
            raise ParseError(_('Empty alternatives.'))

        counter = 0
        for alternative in data.get('alternatives', []):
            if alternative['is_correct'] is True:
                counter += 1

        if counter != 1:
            raise ParseError(_('You must enter one correct alternative.'))

        return data

    def create_alternatives(self, alternatives, question):
        """
        Cria as alternativas passadas.
        """

        logging.info(f"Alternativas: {alternatives}")

        for alternative in alternatives:
            result = Alternative.objects.create(
                **alternative,
                question=question
            )
            question.alternatives.add(result)

    def create(self, validated_data):
        """
        Criando a questão
        """

        logging.info("Criando uma questão.")

        data = self.validate_creation(validated_data)

        logging.info(f"Dados validados: {data}")

        alternatives = data.get('alternatives', [])
        del data['alternatives']

        question = Question.objects.create(**data)
        self.create_alternatives(alternatives, question)

        logging.info(f"Questão: {convert_to_json(question)}")

        logging.info("Questão criada com sucesso!")

        return question
