from django.utils.translation import ugettext_lazy as _
from rest_framework.serializers import (
    ModelSerializer, CharField, DateTimeField, ValidationError,
    SerializerMethodField
)
from django.contrib.auth import get_user_model

# Get the custom user from settings
User = get_user_model()


class UserSerializer(ModelSerializer):
    """
    A serializer for our user profile objects.
    """

    short_name = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'name', 'short_name',
            'is_teacher', 'photo', 'last_login',
            'created_at', 'updated_at'
        )
        extra_kwargs = {'is_teacher': {'read_only': True}}

    def get_short_name(self, obj):
        """
        Get the short name of user.
        """

        return obj.short_name

    def update(self, instance, validated_data):
        """
        Update the user password.
        """

        instance.email = validated_data['email']
        instance.name = validated_data['name']

        if 'photo' in validated_data.keys():
            instance.photo = validated_data['photo']

        instance.save()

        return instance


class UserPasswordSerializer(ModelSerializer):
    """
    A serializer to edit user password.
    """

    password = CharField(write_only=True, style={'input_type': 'password'})

    new_password = CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    confirm_password = CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('password', 'new_password', 'confirm_password')

    def update(self, instance, validated_data):
        """
        Update the user password.
        """

        password = validated_data['password']
        new_password = validated_data['new_password']
        confirm_password = validated_data['confirm_password']

        # Verify if new password and confirm password match.
        if new_password != confirm_password:
            raise ValidationError(_('The new passwords do not match.'))

        # Verify if the old password is correct.
        if not instance.check_password(password):
            raise ValidationError(_('Old password invalid.'))

        instance.set_password(new_password)

        instance.save()

        return instance


class UserRegisterSerializer(ModelSerializer):
    """
    A serializer to register a new user.
    """

    password = CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    confirm_password = CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    last_login = DateTimeField(
        read_only=True
    )

    class Meta:
        model = User
        fields = (
            'id', 'name', 'email', 'short_name',
            'is_teacher', 'photo', 'last_login',
            'created_at', 'updated_at', 'password',
            'confirm_password'
        )

    def validate(self, data):
        """
        Validate if existis another user with same email address and verify
        if the password not match.
        """

        email = data['email']
        password = data['password']
        confirm_password = data['confirm_password']

        # Verify if exists another user with same email address
        user = User.objects.filter(email=email)
        if user.exists():
            raise ValidationError(_('This user has already registered.'))

        # Verify if the passwords not match.
        if password != confirm_password:
            raise ValidationError(_('The passwords do not match.'))

        return data

    def create(self, validated_data):
        """
        Create and return a new user.
        """

        user = User(
            email=validated_data['email'],
            name=validated_data['name'],
            is_teacher=validated_data['is_teacher']
        )

        if 'photo' in validated_data.keys():
            user.photo = validated_data['photo']

        user.set_password(validated_data['password'])
        user.save()

        return user
