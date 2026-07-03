from django.contrib import messages
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

        print("Ticker:", ticker)
        print("Asset Type:", asset_type)
        print("Condition:", condition)
        print("Target Price:", target_price)
        Alert.objects.create(
            user=request.user,
            ticker=ticker,
            asset_type=asset_type,
            condition=condition,
            target_price=target_price
        )

        messages.success(
            request,
            "Alert created successfully!"
        )
        return redirect("/dashboard/")
    

    