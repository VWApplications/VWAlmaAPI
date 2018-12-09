"""
Atributos: queryset, serializer_class, permission_classes,
lookup_field, lookup_url_kwarg

lookup_field é para trocar a busca no parâmetro, pode ir do ID para qualquer outro atributo,
por exemplo o nome. Ex: lookup_field = 'username' -> http://.../users/victorhad/ ao invés de
http://.../users/1/ esse atributo precisa ser único.

Métodos: get_serializer(), get_serializer_context(), get_object().

Ações: list(GET), create(POST), destroy(DELETE), retrieve(GET), update(PUT), partial_update(PATCH)
"""

from rest_framework.views import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import (
    UserSerializer, UserRegisterSerializer, UserPasswordSerializer
)
from django.contrib.auth import get_user_model
from .permissions import UpdateOwnProfile, CreateListUserPermission


# Get the custom user from settings
User = get_user_model()


class UserViewSet(ModelViewSet):
    """
    View set to user.
    """

    filter_backends = (filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend)
    filterset_fields = ('is_teacher',)
    ordering_fields = ('name', 'email')
    search_fields = ('name', 'email')
    ordering = ('name',)

    def get_queryset(self):
        """
        Get query string paramns and filter users.
        http://.../users/?name=Pedro%Calile&email=pedro@gmail.com
        """

        id = self.request.query_params.get('id', None)
        name = self.request.query_params.get('name', None)
        email = self.request.query_params.get('email', None)

        users = User.objects.all()

        if id:
            users = users.filter(pk=id)

        if name:
            users = users.filter(name__icontains=name)

        if email:
            users = users.filter(email__icontains=email)

        return users  # Lazyload, only here we get the users from database

    def get_serializer_class(self):
        """
        Return a serializer class based on action

        actions: list, create, destroy, retrieve, update, partial_update
        """

        if self.action == 'list' or self.action == 'create':
            return UserRegisterSerializer
        elif self.action == 'set_password':
            return UserPasswordSerializer

        return UserSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.

        actions: list, create, destroy, retrieve, update, partial_update
        """

        if self.action == 'list' or self.action == 'create':
            permission_classes = [CreateListUserPermission]
        else:
            permission_classes = [IsAuthenticated, UpdateOwnProfile]

        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['put'], url_path="change-password", url_name="change-password")
    def set_password(self, request, pk=None):
        """
        Controller that allows a logged-in user to edit your own password.
        """

        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.update(user, request.data)
            return Response({'status': 'password set'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)