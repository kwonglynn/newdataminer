from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Module
from .forms import ModuleForm


# Create your views here.
def index(request):
    return render(request, 'mypython/index.html')

def conda(request):
    return render(request, 'mypython/conda.html')

def ddns(request):
    return render(request, 'mypython/ddns.html')

def module_form(request):
    submitted = False
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/python/module_form/?submitted=True')
    else:
        form = ModuleForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'mypython/Module_form.html',
                  {'form':form, 'submitted': submitted})

class ModuleListView(ListView):
    model = Module
    # The default value for contxt_object_name is model's name in lower case + "_list"
    # In this case, the default name is module_list
    # The default template name for ListView is module_list.html.
    context_object_name = 'all_modules'

class ModuleDetailView(DetailView):
    model = Module
    context_object_name = 'module'
    slug_field = 'title'
    slug_url_kwarg = 'title'
    # template_name = "module_detail.html"
