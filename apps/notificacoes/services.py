from django.core.mail import send_mail
from django.conf import settings


def enviar_email(destinatarios, assunto, mensagem):
    if not isinstance(destinatarios, list):
        destinatarios = [destinatarios]

    send_mail(
        subject=assunto,
        message=mensagem,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=destinatarios,
        fail_silently=False,
    )
