from django.shortcuts import render
from django.http import HttpResponse
from alerts.models import Alert
from django.contrib.auth.decorators import login_required

# Create your views here.
def landing(request):
    return render(
        request,
        "dashboard/landing.html"
    )

@login_required
def home(request):
    alerts=Alert.objects.all()
    return render(
        request,
        "dashboard/home.html",
        {
            "alerts":alerts
        }
    )
