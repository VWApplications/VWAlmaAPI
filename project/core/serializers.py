from rest_framework.serializers import ModelSerializer
from .models import News, Tag


class TagSerializer(ModelSerializer):
    """
    A serializer for our tags objects.
    """

    class Meta:
        model = Tag
        fields = '__all__'


class NewsCreateTagsSerializer(ModelSerializer):
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

        for tag in tags:
            result = Tag.objects.create(**tag)
            news.tags.add(result)

    def create(self, validated_data):
        """
        Create news with tags
        """

        tags = validated_data['tags']
        del validated_data['tags']

        news = News.objects.create(**validated_data)
        self.create_tags(tags, news)

        return news


class NewsExistsTagsCreateSerializer(ModelSerializer):
    """
    Create news with existing tags
    """

    class Meta:
        model = News
        fields = ['id', 'title', 'description', 'image', 'link', 'tags']

    def create(self, validated_data):
        """
        Create news with tags
        """

        news = News(
            title=validated_data['title'],
            description=validated_data['description'],
            link=validated_data['link']
        )

        if 'image' in validated_data.keys():
            news.image = validated_data['image']

        news.save()

        news.tags.set(validated_data['tags'])

        return news


class NewsUpdateSerializer(ModelSerializer):
    """
    A serializer for our news objects.
    """

    class Meta:
        model = News
        fields = ['id', 'title', 'description', 'image', 'link', 'tags']

    def update(self, instance, validated_data):
        """
        Update the user password.
        """

        instance.title = validated_data['title']
        instance.description = validated_data['description']
        instance.link = validated_data['link']
        instance.tags.set(validated_data['tags'])

        if 'image' in validated_data.keys():
            instance.image = validated_data['image']

        instance.save()

        return instance
