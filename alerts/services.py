from .models import Alert
from .utils import get_live_price
from .notifications import send_alert_email

def check_all_alerts():
    print(">>> check_all_alerts() started")
    alerts=Alert.objects.filter(is_active=True)
    for alert in alerts:
        price=get_live_price(alert.yahoo_symbol)
        if price is None:
            continue

        if alert.condition=="below":
            is_triggered=price<=alert.target_price
        else:
            is_triggered=price>=alert.target_price

        if is_triggered and not alert.notification_sent:
            send_alert_email(alert)
            alert.notification_sent=True

        alert.triggered=is_triggered    

        alert.save()

        print(alert.company, alert.yahoo_symbol, price)

