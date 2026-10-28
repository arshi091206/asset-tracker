import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "asset_tracker.settings"
)

django.setup()

from django.core.mail import send_mail
from django.conf import settings

send_mail(
    subject="Test Email",
    message="This is a test email sent from Django.",
    from_email=settings.EMAIL_HOST_USER,
    recipient_list=[settings.EMAIL_HOST_USER],
    fail_silently=False
    )

print("Test email sent successfully.")