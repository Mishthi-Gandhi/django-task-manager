from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Task
def login_view(request):
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect("home")
        else:
            return render(request,"login.html",{"error":"Invalid credentials"})

    return render(request,"login.html")
def signup_view(request):
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user=User.objects.create_user(username=username,password=password)
        login(request,user)
        return redirect('home')
    return render(request,"signup.html")

def logout_view(request):
    logout(request)
    return redirect("login")
@login_required
def index(request):
    if request.method=="POST":
        title=request.POST["title"]
        new_task=Task.objects.create(title=title,user=request.user)
        new_task.save()
        return redirect('home')
    else:
        tasks=Task.objects.filter(user=request.user)
        return render(request,'home.html',{'tasks':tasks})
def toggle(request,id):
    task=Task.objects.get(id=id)
    task.completed=not task.completed
    task.save()
    return redirect('home')
# Create your views here.

