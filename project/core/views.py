from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter
)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import NewsCreateTagsSerializer, TagSerializer, NewsUpdateSerializer, NewsExistsTagsCreateSerializer
from .models import News, Tag
from .permissions import CreateUpdateDestroyAdminPermission


class NewsViewSet(ModelViewSet):
    """
    View set to news

    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """

    queryset = News.objects.all()
    permission_classes = (CreateUpdateDestroyAdminPermission,)

    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'tags__title')
    ordering_fields = ('created_at',)

    def get_serializer_class(self):
        """
        Return a serializer class based on action
        """

        if self.action == 'exists_tags':
            return NewsExistsTagsCreateSerializer

        if self.action == 'list' or self.action == 'create':
            return NewsCreateTagsSerializer

        return NewsUpdateSerializer

    @action(methods=['post'], detail=False, url_path="exists-tags")
    def exists_tags(self, request):
        """
        Get existing tags to create a news
        """

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            headers = self.get_success_headers(serializer.data)
            serializer.create(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagsViewSet(ModelViewSet):
    """
    View set to tags.

    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [CreateUpdateDestroyAdminPermission]
