from rest_framework import serializers
from rest_framework.exceptions import ParseError
from .models import Section, ExamConfig
from django.utils import timezone
import logging


class ExamConfigSerializer(serializers.ModelSerializer):
    """
    Serializando os dados das configurações das provas.
    """

    class Meta:
        model = ExamConfig
        fields = ('id', 'title', 'datetime', 'weight', 'duration')


class SectionSerializer(serializers.ModelSerializer):
    """
    Serializado de dados dos grupos da disciplina.
    """

    exam_config = ExamConfigSerializer(many=True)

    class Meta:
        model = Section
        fields = (
            'id', 'title', 'description', 'is_closed',
            'discipline', 'methodology', 'is_finished',
            'exam_config'
        )

    def create_exam_config(self, exam_config):
        """
        Cria as configurações da avaliação.
        """

        configs = []

        weight = 0
        for config in exam_config:
            if "datetime" in config.keys():
                if config['datetime'] < timezone.now():
                    raise ParseError("A data/hora da prova não pode ser menor que a data/hora atual.")

            if "weight" in config.keys():
                weight += config['weight']
            else:
                weight += 10

            configs.append(config)

        if weight != 10:
            raise ParseError("A somatória dos pesos tem que dar 10.")

        return configs

    def create(self, validated_data):
        """
        Cria e retorna uma nova seção.
        """

        logging.info(f"Dados para criação da seção: {validated_data}")

        if "exam_config" not in validated_data.keys():
            raise ParseError("As configurações da prova são obrigatórias.")

        exam_config = validated_data['exam_config']
        del validated_data['exam_config']

        section = Section(**validated_data)

        configs = self.create_exam_config(exam_config)

        section.save()

        for config in configs:
            section.exam_config.add(ExamConfig.objects.create(section=section, **config))

        logging.info("Seção criada com sucesso!")

        return section

    def update(self, instance, validated_data):
        """
        Atualiza os dados do usuário
        """

        logging.info(f"Instancia da seção para atualização: {instance}")
        logging.info(f"Dados para atualização da seção: {validated_data}")

        if "title" in validated_data.keys():
            instance.title = validated_data['title']

        if "description" in validated_data.keys():
            instance.description = validated_data['description']

        if "methodology" in validated_data.keys():
            instance.methodology = validated_data['methodology']

        if "exam_config" in validated_data.keys():
            configs = self.create_exam_config(validated_data['exam_config'])

            instance.exam_config.all().delete()

            for config in configs:
                instance.exam_config.add(ExamConfig.objects.create(section=instance, **config))

        instance.save()

        logging.info("Seção atualizada com sucesso!")

        return instance
