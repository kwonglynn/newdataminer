from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'mypython/index.html')

def remote(request):
    return render(request, 'mypython/remote.html')
