from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.conf import settings
import logging


def send_email_template(subject,
                        template,
                        context,
                        recipient_list,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        fail_silently=False):
    """
    Função para enviar email.
    """

    logging.info("Enviando email.")

    # Gera o template html de email no formato de string
    message_html = render_to_string(template, context)

    # Gera a mensagem removendo as tags html.
    message_txt = strip_tags(message_html)

    # Cria o email com multiplas alternativa para renderizar html
    email = EmailMultiAlternatives(
        subject=subject,
        body=message_txt,
        from_email=from_email,
        to=recipient_list
    )

    # Se o provedor de email aceita formato html, usar ele.
    email.attach_alternative(message_html, "text/html")

    # Se o envio de email falhar, sileciosamente irá disparar uma exceção.
    # Se der tudo certo irá enviar o email
    email.send(fail_silently=fail_silently)

    logging.info("Email enviado!")
