from .models import Alert
from .utils import get_live_price

def check_all_alerts():
    alerts=Alert.objects.filter(is_active=True)
    for alert in alerts:
        if alert.asset_type!="stock":
            continue
        price=get_live_price(alert.ticker+".NS")
        if price is None:
            continue

        if alert.condition=="below":
            is_triggered=price<=alert.target_price
        else:
            is_triggered=price>=alert.target_price

        if is_triggered and not alert.notification_sent:
            print(f"Alert triggered for {alert.ticker} at price {price}")
            alert.notification_sent=True

        alert.triggered=is_triggered    

        alert.save()