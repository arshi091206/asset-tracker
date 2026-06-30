from django.shortcuts import render, redirect
from .models import Alert
from django.contrib.auth.decorators import login_required

@login_required
def create_alert(request):
    if request.method=="GET":
        return render(
            request,
            "alerts/create_alert.html"
        )
    if request.method=="POST":
        ticker=request.POST["ticker"]
        asset_type=request.POST["asset_type"]
        condition=request.POST["condition"]
        target_price=request.POST["target_price"]

        Alert.objects.create(
            ticker=ticker,
            asset_type=asset_type,
            condition=condition,
            target_price=target_price
        )
        return redirect("/dashboard/")
    