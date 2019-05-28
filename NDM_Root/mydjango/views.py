from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "mydjango/index.html")

def postgres(request):
    return render(request, "mydjango/postgres.html")

def mysql(request):
    return render(request, "mydjango/mysql.html")

def user(request):
    return render(request, "mydjango/user.html")

def background(request):
    return render(request, "mydjango/background_task.html")

def channels(request):
    return render(request, "mydjango/channels.html")
