from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from .serializers import NewsTagsSerializer, TagSerializer
from .models import News, Tag
from .permissions import CreateUpdateDestroyAdminPermission


class CustomPagination(PageNumberPagination):
    """
    Separar a lista de tickets em páginas.
    """

    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


class NewsViewSet(ModelViewSet):
    """
    View set to news

    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """

    serializer_class = NewsTagsSerializer
    permission_classes = (CreateUpdateDestroyAdminPermission,)
    pagination_class = CustomPagination

    def get_queryset(self):
        """
        Make a filter if passed, otherwise return all news.
        """

        queryset = News.objects.all()

        search = self.request.query_params.get('search', None)
        tag = self.request.query_params.get('tag', None)

        if search:
            queryset = queryset.filter(title__icontains=search)

        if tag:
            queryset = queryset.filter(tags__title__icontains=tag)

        return queryset


class TagsViewSet(ModelViewSet):
    """
    View set to tags.

    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (CreateUpdateDestroyAdminPermission,)
