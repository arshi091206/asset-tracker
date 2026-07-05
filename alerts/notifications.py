from django.core.mail import send_mail
from django.conf import settings

def send_alert_email(alert):
    subject=f"Alert Triggered for {alert.ticker}"
    message=f"""
    Hello {alert.user.username},
    Your alert has been triggered!
    Ticker: {alert.ticker}
    Condition: {alert.condition}
    Target Price: ₹{alert.target_price}

    Open Asset Tracker to manage your alerts.

    Regards,
    Asset Tracker Team
    """
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[alert.user.email],
        fail_silently=False
    )