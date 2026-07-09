from django.shortcuts import render
from django.http import HttpResponse
from alerts.models import Alert
from django.contrib.auth.decorators import login_required
from alerts.utils import get_live_price

# Create your views here.
def landing(request):
    return render(
        request,
        "dashboard/landing.html"
    )

@login_required
def home(request):
    alerts=Alert.objects.filter(
        user=request.user
    )
    for alert in alerts:
        alert.live_price=get_live_price(alert.yahoo_symbol)

        if alert.live_price:
            if alert.condition=="below":
                alert.triggered=(
                    alert.live_price<=alert.target_price
                )
            else:
                alert.triggered=(
                    alert.live_price>=alert.target_price
                )
        else:
            alert.triggered=False
    return render(
        request,
        "dashboard/home.html",
        {
            "alerts":alerts
        }
    )
