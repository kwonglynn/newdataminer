from django.shortcuts import render, HttpResponseRedirect

def index(request):
    return render(request, "myserver/index.html")
