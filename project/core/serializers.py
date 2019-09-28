from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import News, Tag
import logging


class TagSerializer(ModelSerializer):
    """
    Um serializador para nossos objetos de tags.
    """

    class Meta:
        model = Tag
        fields = ['id', 'title']


class NewsTagsSerializer(ModelSerializer):
    """
    Serializado para criar notícias com novas tags
    """

    tags = TagSerializer(many=True, required=False)
    created_at = SerializerMethodField()

    class Meta:
        model = News
        fields = ['id', 'title', 'description', 'image', 'link', 'tags', 'created_at']

    def get_created_at(self, obj):
        """
        Pega a data de criação da notícia formatada.
        """

        return obj.format_datetime(obj.created_at)

    def create_tags(self, tags, news):
        """
        Cria a tag.
        """

        logging.info("Tags: " + str(tags))

        for tag in tags:
            result, _ = Tag.objects.get_or_create(**tag)
            news.tags.add(result)

    def create(self, validated_data):
        """
        Cria a notícia.
        """

        logging.info("Criando uma notícia.")

        logging.info("Dados validados: " + str(validated_data))

        tags = validated_data.get('tags', [])
        del validated_data['tags']

        news = News.objects.create(**validated_data)
        self.create_tags(tags, news)

        logging.info(news)

        return news

    def update(self, instance, validated_data):
        """
        Atualiza a notícia.
        """

        logging.info("Atualizando a notícia " + str(instance.title))

        logging.info("Dados de atualização: " + str(validated_data))

        if "title" in validated_data.keys():
            instance.title = validated_data['title']

        if "description" in validated_data.keys():
            instance.description = validated_data['description']

        if "link" in validated_data.keys():
            instance.link = validated_data['link']

        if "tags" in validated_data.keys():
            tags = validated_data.get('tags', [])
            self.create_tags(tags, instance)

        if 'image' in validated_data.keys():
            instance.image = validated_data['image']

        instance.save()

        return instance
