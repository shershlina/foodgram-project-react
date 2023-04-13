from django.conf import settings
from django.core.mail import send_mail


def send_email(email, confirmation_code):
    return send_mail(
        subject='Код подтверждения',
        message=('Регистрация прошла успешно! '
                 f'Код подтверждения: {confirmation_code}'),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
