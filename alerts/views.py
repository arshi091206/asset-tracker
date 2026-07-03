from django.contrib import messages
from django.shortcuts import render, redirect,get_object_or_404
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
    

@login_required
def delete_alert(request, alert_id):
    alert=get_object_or_404(
        Alert,
        id=alert_id,
        user=request.user
    )

    alert.delete()

    messages.success(
        request,
        "Alert deleted successfully"
    )

    return redirect("/dashboard/")

@login_required
def edit_alert(request, alert_id):
    alert=get_object_or_404(
        Alert,
        id=alert_id,
        user=request.user
    )

    if request.method=="GET":
        return render(
            request,
            "alerts/edit_alert.html",
            {
                "alert":alert
            }
        )
    
    if request.method=="POST":
        alert.ticker=request.POST["ticker"]
        alert.asset_type=request.POST["asset_type"]
        alert.condition=request.POST["condition"]
        alert.target_price=request.POST["target_price"]

        alert.save()

        messages.success(
            request,
            "Alert updated successfully!"
        )

        return redirect("/dashboard/")