from rest_framework.viewsets import ModelViewSet
from common.utils import convert_to_json
from core.views import CustomPagination
from disciplines.models import Discipline
from sections.models import Section
import logging


class GenericViewSet(ModelViewSet):
    """
    View generica.
    """

    pagination_class = CustomPagination

    def hasDataKeys(self):
        """
        Verifica se a requisição tem determinados
        data keys.
        """

        if ("disciplineID" in self.request.data.keys() or
            "sessionID" in self.request.data.keys()):
            return True

        return False

    def change_action(self):
        """
        Modifica a action para list caso precise.
        """

        if self.action == 'create' and self.hasDataKeys():
            self.action = "list"

    def create(self, request, *args, **kwargs):
        """
        Se for passado o atributo disciplineID irá dispará
        a ação de listagem, caso contrário irá dispará a
        ação de criação.
        """

        logging.info(f"Payload: {request.data}")

        if self.hasDataKeys():
            logging.info("Objeto listado com sucesso!")
            return super().list(request, *args, **kwargs)

        logging.info("Objeto criado com sucesso!")
        return super().create(request, *args, **kwargs)

    def get_discipline(self):
        """
        Pega a disciplina passada por parâmetro.
        """

        disciplineID = self.request.data.get('disciplineID', None)
        if self.action == 'create':
            disciplineID = self.request.data.get('discipline', None)

        try:
            discipline = Discipline.objects.get(id=disciplineID)
            logging.info(f"Disciplina: {convert_to_json(discipline)}")
        except Discipline.DoesNotExist:
            return False

        return discipline

    def get_section(self):
        """
        Pega a sessão da disciplina passada por parâmetro.
        """

        sectionID = self.request.data.get('sectionID', None)
        if self.action == 'create':
            sectionID = self.request.data.get('section', None)

        try:
            section = Section.objects.get(id=disciplineID)
            logging.info(f"Seção: {convert_to_json(section)}")
        except Section.DoesNotExist:
            return False

        return section