from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

def register(request):
    if request.method=="GET":
        return render(request,"accounts/register.html")
    
    if request.method=="POST":
        username=request.POST["username"].strip()
        email=request.POST["email"].strip()
        password=request.POST["password"]

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose another.")
            return render(request, "accounts/register.html")

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Account created successfully!")
        return redirect("/login/")
    
def login_view(request):
    if request.method=="GET":
        return render(request,"accounts/login.html")
    
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        
        user=authenticate(
            request,
            username=username,
            password=password
        )
        print(user)

        if user is not None:
            login(request,user)
            return redirect("/dashboard/")
        
        messages.error(
            request,
            "Invalid username or password."
        )

        return redirect("/login/")
    
def logout_view(request):
    logout(request)
    return redirect("/")