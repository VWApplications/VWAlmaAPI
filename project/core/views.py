from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from .serializers import NewsTagsSerializer, TagSerializer
from .models import News, Tag
from .permissions import CreateUpdateDestroyAdminPermission
import logging


class CustomPagination(PageNumberPagination):
    """
    Separar a lista de tickets em páginas.
    """

    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


class NewsViewSet(ModelViewSet):
    """
    Views de notícias.
    """

    serializer_class = NewsTagsSerializer
    permission_classes = (CreateUpdateDestroyAdminPermission,)
    pagination_class = CustomPagination

    def get_queryset(self):
        """
        Faça um filtro, se aprovado, retorne todas as notícias fitradas.
        """

        logging.info("Buscando notícias.")

        queryset = News.objects.all()

        search = self.request.query_params.get('search', None)
        tag = self.request.query_params.get('tag', None)

        logging.info("Filtros: " + str({"search": search, "tag": tag}))

        if search:
            queryset = queryset.filter(title__icontains=search)
            logging.info("Notícias filtradas pela pesquisa: " + str(queryset))

        if tag:
            queryset = queryset.filter(tags__title__icontains=tag)
            logging.info("Notícias filtradas pela tag: " + str(queryset))

        return queryset


class TagsViewSet(ModelViewSet):
    """
    Views de Tags
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (CreateUpdateDestroyAdminPermission,)
