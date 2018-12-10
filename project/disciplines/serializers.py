from rest_framework.serializers import (
    ModelSerializer, CharField
)
from django.contrib.auth import get_user_model
from .models import Discipline

# Get the custom user from settings
User = get_user_model()


class UserDisciplineSerializer(ModelSerializer):
    """
    Serializer to show teacher into discipline serializer
    """

    class Meta:
        model = User
        fields = ('id', 'short_name', 'email')


class DisciplineSerializer(ModelSerializer):
    """
    A serializer to list and register a new discipline.
    """

    teacher = UserDisciplineSerializer(read_only=True)

    password = CharField(write_only=True)

    class Meta:
        model = Discipline
        fields = (
            'id', 'title', 'description', 'course', 'teacher',
            'classroom', 'password', 'students', 'monitors',
            'students_limit', 'monitors_limit', 'is_closed'
        )
        read_only_fields = ('students', 'monitors')

    def current_user(self):
        """
        Method to get the current teacher logged.
        """

        teacher = self.context['request'].user.id
        return teacher

    def create(self, validated_data):
        """
        Create and return a new discipline
        """

        teacher = User.objects.get(id=self.current_user())

        discipline = Discipline.objects.create(
            **validated_data,
            teacher=teacher
        )

        discipline.save()

        return discipline