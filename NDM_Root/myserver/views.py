from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Dict
# from .forms import DictForm

from django.db.models import Q

# For searching and return the new word.
import os
import re
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
    word = request.GET.get('q4')
    try:
        word = word.strip().split()[0]
        word = word.lower()
    except:
        return HttpResponseRedirect(reverse('myserver:dict_list'))
    # Judge if the word has already been added:
    if Dict.objects.filter(word=word).exists():
        dict = Dict.objects.filter(word=word)[0]
        return HttpResponseRedirect(reverse('myserver:dict_detail', kwargs={'pk': dict.pk}))
    else:
        cwd = os.getcwd()
        ## Work in the dict directory.
        dict_dir = r'C:\Google\Work\MyWebsite\newdataminer\NDM_Root\myserver\dict'
        os.chdir(dict_dir)
        username = request.user.username
        result_file_name = username + '.json'
        # Delete the result json file it already exists.
        if os.path.isfile(result_file_name):
            os.remove(result_file_name)

        os.system("conda activate django2 | scrapy crawl dict -o %s -a word=%s" % (result_file_name, word))

        while True:
            if os.path.isfile(result_file_name):
                if os.path.getsize(result_file_name) > 0:
                    with open(result_file_name, 'r') as fi:
                        lines = fi.readlines()
                        result_json = lines[1].strip()
                        result_dict = json.loads(result_json)
                        word = result_dict['word']
                        pron = result_dict['pron']
                        morf = result_dict['morf']
                        forms = result_dict['form']
                        trans_list = json.loads(result_dict['trans'])
                        trans_list = trans_list[0] # Only take the first translation for now.
                        trans = ''
                        for item in trans_list[:2]:
                            if not re.search('[0-9]', item):
                                trans += item + ' '
                        break
                else:
                    return HttpResponseRedirect(reverse('myserver:dict_list'))
            else:
                time.sleep(1)

        dict = Dict.objects.get_or_create(word=word, pron=pron, morf=morf, forms=forms, trans=trans)[0]
        dict.added_by = request.user
        dict.save()

        ## Go back the original directory.
        os.chdir(cwd)
        return HttpResponseRedirect(reverse('myserver:dict_detail', kwargs={'pk': dict.pk}))

class DictListView(LoginRequiredMixin, ListView):
    model = Dict
    template_name = 'myserver/dict_list.html'
    paginate_by = 50

    def get_queryset(self):
        object_list = Dict.objects.filter(Q(label__icontains = self.request.user.username)
        ).order_by('word')

        return object_list

class DictDetailView(DetailView):
    model = Dict

class DictDeleteView(PermissionRequiredMixin, DeleteView):
    model = Dict
    permission_required = "dict.can_publish_delete"
    success_url = reverse_lazy('myserver:dict_list')  # Remember to use the app name prefix.

# Delete directly!
# @login_required
# def delete_word(request, pk):
#     Dict.objects.filter(pk=pk).delete()
#     return HttpResponseRedirect(reverse('myserver:dict_list'))

@login_required
def remove_word(request, pk):
    object = get_object_or_404(Dict, pk=pk)
    username = request.user.username
    object.remove(username)
    return redirect('myserver:dict_list')

@login_required
def add_to_dict(request, pk):
    object = get_object_or_404(Dict, pk=pk)
    username = request.user.username
    object.add(username)
    return redirect('myserver:dict_list')
