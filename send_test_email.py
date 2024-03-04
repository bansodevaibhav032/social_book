# Create a management command, e.g., send_test_email.py
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'Send a test email'

    def handle(self, *args, **kwargs):
        send_mail(
            'Test Subject',
            'Test Message',
            settings.EMAIL_HOST_USER,
            ['recipient@example.com'],
            fail_silently=False,
        )
