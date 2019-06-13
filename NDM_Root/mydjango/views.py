from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "mydjango/index.html")

def model(request):
    return render(request, "mydjango/model.html")

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

def email_server(request):
    return render(request, "mydjango/email_server.html")

def slug(request):
    return render(request, "mydjango/slug.html")

def use_js(request):
    return render(request, "mydjango/use_js.html")

def use_Q(request):
    return render(request, "mydjango/use_Q.html")

def use_haystack(request):
    return render(request, "mydjango/use_haystack.html")

def use_GSE(request):
    return render(request, "mydjango/use_GSE.html")
