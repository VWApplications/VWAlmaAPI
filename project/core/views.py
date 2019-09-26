from rest_framework.viewsets import ModelViewSet
from .serializers import NewsTagsSerializer, TagSerializer
from .models import News, Tag
from .permissions import CreateUpdateDestroyAdminPermission


class NewsViewSet(ModelViewSet):
    """
    View set to news

    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """

    queryset = News.objects.all()
    serializer_class = NewsTagsSerializer
    permission_classes = (CreateUpdateDestroyAdminPermission,)


class TagsViewSet(ModelViewSet):
    """
    View set to tags.

    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (CreateUpdateDestroyAdminPermission,)
