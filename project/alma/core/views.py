from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from common.generic_view import CustomPagination
from common.email import send_email_template
from .serializers import NewsTagsSerializer, TagSerializer
from .models import News, Tag
from .permissions import CreateUpdateDestroyAdminPermission
import logging


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
            raise ParseError("Email é obrigatório.")

        if "name" not in request.data:
            raise ParseError("Nome é obrigatório.")

        if "message" not in request.data:
            raise ParseError("Mensagem é obrigatório.")

        # Envia o email
        send_email_template(
            subject="Mensagem da plataforma ALMA.",
            template='email.html',
            from_email=request.data['email'],
            context={
                'name': request.data['name'],
                'email': request.data['email'],
                'message': request.data['message']
            },
            recipient_list=["vwapplication@gmail.com"]
        )

        logging.info("Email enviado com sucesso!")

        return Response({'success': True}, status=status.HTTP_200_OK)