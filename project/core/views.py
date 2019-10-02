from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from common.email import send_email_template
from django.conf import settings
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


class ContactViewSet(APIView):
    """
    View para realizar contato com o administrador.
    """

    def post(self, request, *args, **kwargs):
        """
        Pega os dados do formulário e manda o email.
        """

        logging.info("Enviando uma mensagem para o administrador")
        logging.info("Payload: " + str(request.data))

        if "email" not in request.data:
            raise ParseError(_("Email is required."))

        if "name" not in request.data:
            raise ParseError(_("Name is required."))

        if "message" not in request.data:
            raise ParseError(_("Message is required."))

        # Envia o email
        send_email_template(
            subject=_('Contact from ALMA Plataform'),
            template='email.html',
            from_email="mailgun@sandbox43d3bc2d2ec44a6688b52d324f1f7cb3.mailgun.org",
            context={
                'name': request.data['name'],
                'email': request.data['email'],
                'message': request.data['message']
            },
            recipient_list=[settings.DEFAULT_FROM_EMAIL]
        )

        logging.info("Email enviado com sucesso!")

        return Response({'success': True}, status=status.HTTP_200_OK)