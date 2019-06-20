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

import operator
from django.db.models import Q
from functools import reduce

# For searching and return the new word.
import os
import re
import json
import datetime, time

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
        if 'table' in request.path:
            return redirect('myserver:dict_list_table')
        elif 'card' in request.path:
            return redirect('myserver:dict_list_card')
    # Judge if the word has already been added:
    if Dict.objects.filter(word=word).exists():
        dict = Dict.objects.filter(word=word)[0]
        return HttpResponseRedirect(reverse('myserver:dict_detail_card', kwargs={'pk': dict.pk}))
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
                        if word.endswith('*'):
                            word = word[:-1]
                        pron = result_dict['pron']
                        morf = result_dict['morf']
                        forms = result_dict['form']
                        trans_list = json.loads(result_dict['trans'])
                        trans_list = trans_list[0] # Only take the first translation for now.
                        trans = ''
                        for item in trans_list[:2]:
                            if not re.search('[0-9]', item):
                                trans += item + ' '

                        accordion_id = "accordion" + "_" + word
                        heading_id = "heading" + "_" + word
                        collapse_id = "collaspse" + "_" + word

                        break
                else:
                    if 'table' in request.path:
                        return redirect('myserver:dict_list_table')
                    elif 'card' in request.path:
                        return redirect('myserver:dict_list_card')
            else:
                time.sleep(1)

        dict = Dict.objects.get_or_create(word=word, pron=pron, morf=morf,
                                          forms=forms, trans=trans,
                                          accordion_id=accordion_id,
                                          heading_id=heading_id,
                                          collapse_id=collapse_id,
                                          )[0]
        dict.added_by = request.user
        dict.save()

        ## Go back the original directory.
        os.chdir(cwd)
        path = request.META.get('HTTP_REFERER')
        if 'table' in path:
            return HttpResponseRedirect(reverse('myserver:dict_detail_table', kwargs={'pk': dict.pk}))
        elif 'card' in path:
            return HttpResponseRedirect(reverse('myserver:dict_detail_card', kwargs={'pk': dict.pk}))


class DictListView(LoginRequiredMixin, ListView):
    model = Dict
    paginate_by = 20

    total = 0
    total_today = 0

    def get_queryset(self):

        if 'table' in self.request.path:
            self.template_name = 'myserver/dict_list_table.html'
        elif 'card' in self.request.path:
            self.template_name = 'myserver/dict_list_card.html'

        # The all the user's list:
        all_list = Dict.objects.filter(Q(name_label__icontains = self.request.user.username)).order_by('word')
        self.total = all_list.count()

        # For today's list of user:
        now = datetime.datetime.now()
        Q_list = [Q(name_label__icontains = self.request.user.username),
                  Q(last_date__year = now.year),
                  Q(last_date__month = now.month),
                  Q(last_date__day = now.day)
        ]
        query = reduce(operator.and_, Q_list)
        today_list = Dict.objects.filter(query).order_by('word')
        self.total_today = today_list.count()

        if 'today' in self.request.path:
            object_list = today_list
        else:
            object_list = all_list

        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total"] = self.total
        context["total_today"] = self.total_today
        return context

class DictPracticeListView(LoginRequiredMixin, ListView):
    model = Dict
    template_name = 'myserver/dict_practice.html'
    paginate_by = 1

    total = 0
    total_today = 0

    def get_queryset(self):
        # The all the user's list:
        all_list = Dict.objects.filter(Q(name_label__icontains = self.request.user.username)).order_by('word')
        self.total = all_list.count()

        # For today's list of user:
        now = datetime.datetime.now()
        Q_list = [Q(name_label__icontains = self.request.user.username),
                  Q(last_date__year = now.year),
                  Q(last_date__month = now.month),
                  Q(last_date__day = now.day)
        ]
        query = reduce(operator.and_, Q_list)
        today_list = Dict.objects.filter(query).order_by('word')
        self.total_today = today_list.count()

        if 'today' in self.request.path:
            object_list = today_list
        else:
            object_list = all_list

        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total"] = self.total
        context["total_today"] = self.total_today
        return context

class DictDetailView(DetailView):
    model = Dict

class DictDeleteView(PermissionRequiredMixin, DeleteView):
    model = Dict
    permission_required = "dict.can_publish_delete"
    success_url = reverse_lazy('myserver:dict_list_table')  # Remember to use the app name prefix.

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
    path = request.META.get('HTTP_REFERER')
    if 'table' in path:
        return redirect('myserver:dict_list_table')
    elif 'card' in path:
        return redirect('myserver:dict_list_card')

@login_required
def remember_word(request, pk):
    object = get_object_or_404(Dict, pk=pk)
    username = request.user.username
    object.remove(username)
    path = request.META.get('HTTP_REFERER')
    try:
        if path.endswith('server/swedish/'):
            return redirect('myserver:dict_practice')
        else:
            return redirect(path)
    except:
        return redirect('myserver:dict_practice')

@login_required
def add_to_dict(request, pk):
    object = get_object_or_404(Dict, pk=pk)
    username = request.user.username
    object.add(username)
    path = request.META.get('HTTP_REFERER')
    if 'table' in path:
        return redirect('myserver:dict_list_table')
    elif 'card' in path:
        return redirect('myserver:dict_list_card')
