from django.views.generic import View
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint.fonts import FontConfiguration
from django.conf import settings
from weasyprint import HTML, CSS
from uuid import uuid4
import os


class GeneratePDFView(View):
    """
    Classe reponsável por armazenar a foto do usuário.
    """

    def get(self, request, *args, **kwargs):
        """
        Requisição gerar um PDF.
        TODO: Criar utilizando strategy geração de PDFs e Excel passando um
        parametros:

        - type: é o tipo de pdf/excel que será gerado (notas, relatorio, exercicio, ...)
        - name: é o nome do pdf/excel que será baixado. (a partir da extensão vamos definir se é um pdf ou excel)

        De acordo com o tipo passado vamos renderizar um html/css diferente com dados diferentes pego das modelos.
        """

        name = request.GET.get("name")
        file_type = request.GET.get("type")
        print(name, file_type)

        html_string = render_to_string('invoice.html', {'name': "Victor Deon", "email": "victorhad@gmail.com", "message": "Ola mundo!"})

        file_id = uuid4()
        font_config = FontConfiguration()
        html = HTML(string=html_string)
        css = CSS(settings.STATIC_ROOT + '/invoice.css')
        html.write_pdf(f"common/{file_id}.pdf", font_config=font_config, stylesheets=[css])

        with open(f"common/{file_id}.pdf", "rb") as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment;filename=recibo.pdf'
            os.remove(f"common/{file_id}.pdf")

        return response
