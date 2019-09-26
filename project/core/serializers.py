from rest_framework.serializers import ModelSerializer
from .models import News, Tag
import logging


class TagSerializer(ModelSerializer):
    """
    A serializer for our tags objects.
    """

    class Meta:
        model = Tag
        fields = ['id', 'title']


class NewsTagsSerializer(ModelSerializer):
    """
    Create news with new tags
    """

    tags = TagSerializer(many=True)

    class Meta:
        model = News
        fields = ['id', 'title', 'description', 'image', 'link', 'tags']

    def create_tags(self, tags, news):
        """
        Create tags
        """

        logging.info("Tags: " + str(tags))

        for tag in tags:
            result, _ = Tag.objects.get_or_create(**tag)
            news.tags.add(result)

    def create(self, validated_data):
        """
        Create news with tags
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
        Update the user password.
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
