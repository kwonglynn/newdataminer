from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Dict
from .forms import DictForm

from django.db.models import Q

# For searching and return the new word.
import os
import json
import time
# Configure settings for project
# Need to run this before calling models from application!
os.environ.setdefault('DJANGO_SETTINGS_MODULE','NDM.settings')

import django
# Import settings
django.setup()

from myserver.models import Dict

#####
@login_required
def index(request):
    return render(request, "myserver/index.html")

@login_required
def dict_create(request):
    cwd = os.getcwd()
    ## Work in the dict directory.
    dict_dir = r'C:\Google\Work\MyWebsite\newdataminer\NDM_Root\myserver\dict'
    username = request.user.username
    result_file_name = username + '.json'
    # Delete the file it already exists.
    if os.path.isfile(result_file_name):
        os.remove(result_file_name)
    word = self.request.GET.get('q4')
    word = word.strip().split()[0]
    os.system("conda activate django2 | scrapy crawl dict -o %s -a word=%s" % (result_file_name, word))
    ## Go back the original directory.
    os.chdir(cwd)

    while True:
        if os.path.isfile(result_file_name):
            with open(result_file_name, 'r') as fi:
                lines = fi.readlines()
                result_json = lines[1].strip()
                result_dict = json.loads(result_json)
                pron = result_dict['pron']
                morf = result_dict['morf']
                trans = result_dict['trans']
                phrase = result_dict['phrase']
                break
        else:
            time.sleep(1)

    dict = Dict.objects.get_or_create(word=word, pron=pron, morf=morf, trans=trans, phrase=phrase)[0]
    dict.added_by = request.user
    dict.save()

    return redirect('dict:dict_draft_list' pk=dict.pk)

class DictListView(ListView):
    model = Dict
    template_name = 'dict/dict_list.html'
    paginate_by = 50

    def get_queryset(self):
        query = self.request.GET.get('q4', '')
        object_list = Dict.objects.filter(
            Q(published_date__lte=timezone.now()) & Q(title__icontains=query)
        ).order_by('title')

        return object_list

class DictDetailView(DetailView):
    model = Dict

class DictCreateView(PermissionRequiredMixin, CreateView):
    model = Dict
    form_class = DictForm
    permission_required = "dict.can_publish_delete"

class DictUpdateView(LoginRequiredMixin, UpdateView):
    model = Dict
    form_class = DictForm

    # The post needs to be re-published if it is updated.
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.published_date = None
        self.object.save()
        return super().form_valid(form)

class DictDeleteView(PermissionRequiredMixin, DeleteView):
    model = Dict
    permission_required = "dict.can_publish_delete"
    success_url = reverse_lazy('dict:dict_list')  # Remember to use the app name prefix.

@login_required
def publish(request, pk):
    object = get_object_or_404(Dict, pk=pk)
    object.publish()
    return redirect('dict:dict_list')
