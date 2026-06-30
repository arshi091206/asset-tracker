from django.shortcuts import render
from django.http import HttpResponse
from alerts.models import Alert

# Create your views here.
def landing(request):
    return render(
        request,
        "dashboard/landing.html"
    )

def home(request):
    print(request.user)

    alerts=Alert.objecets.all()
    return render(
        request,
        "dashboard/home.html",
        {
            "alerts":alerts
        }
    )
