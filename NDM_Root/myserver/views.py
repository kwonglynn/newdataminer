from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Dict
from .forms import DictForm

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

#####
@login_required
def index(request):
    return render(request, "myserver/index.html")

@login_required
def dict_create(request):
    word = request.GET.get('q4', '')
    try:
        word = word.strip().split()[0]
        word = word.lower()
    except:
        if 'table' in request.META.get('HTTP_REFERER'):
            return redirect('myserver:dict_list_table_today')
        elif 'card' in request.META.get('HTTP_REFERER'):
            return redirect('myserver:dict_list_card_today')

    # Judge if the word has already been added:
    if Dict.objects.filter(word=word).exists():
        dict = Dict.objects.filter(word=word)[0]

        if 'table' in request.META.get('HTTP_REFERER'):
            return HttpResponseRedirect(reverse('myserver:dict_detail_table', kwargs={'pk': dict.pk}))
        elif 'card' in request.META.get('HTTP_REFERER'):
            return HttpResponseRedirect(reverse('myserver:dict_detail_card', kwargs={'pk': dict.pk}))

    else:
        cwd = os.getcwd()
        ## Work in the dict directory.
        # Local
        dict_dir = r'C:\Google\Work\MyWebsite\newdataminer\NDM_Root\myserver\dict'
        # PythonAnyWhere
        # dict_dir = r'/home/guanglin/newdataminer/NDM_Root/myserver/dict'
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
                    if 'table' in request.META.get('HTTP_REFERER'):
                        return redirect('myserver:dict_list_table_today')
                    elif 'card' in request.META.get('HTTP_REFERER'):
                        return redirect('myserver:dict_list_card_today')
            else:
                time.sleep(1)

        dict = Dict(word=word, pron=pron, morf=morf,
                    forms=forms, trans=trans,
                    accordion_id=accordion_id,
                    heading_id=heading_id,
                    collapse_id=collapse_id,
                    )
        dict.added_by = request.user
        dict.save()

        ## Go back the original directory.
        os.chdir(cwd)

        if 'table' in request.META.get('HTTP_REFERER'):
            return HttpResponseRedirect(reverse('myserver:dict_detail_table', kwargs={'pk': dict.pk}))
        elif 'card' in request.META.get('HTTP_REFERER'):
            return HttpResponseRedirect(reverse('myserver:dict_detail_card', kwargs={'pk': dict.pk}))

@login_required
def dict_update_create(request, pk):
    dict1 = Dict.objects.filter(pk=pk)[0]

    # For the orginal word, remove the label so that it is not redundant with the new one.
    dict1.name_label = dict1.name_label.replace(request.user.username + ';', '')
    dict1.last_name_date_label = re.sub("%s_[0-9]*;" % request.user.username, "", dict1.last_name_date_label)
    dict1.save()

    # For the new word, it will replace the old word for the current user. However, it should not influence other users.
    dict2 = Dict(word=dict1.word, added_by=dict1.added_by,
                 pron=dict1.pron, morf=dict1.morf, forms=dict1.forms, trans=dict1.trans,
                 )
    dict2.save()

    if 'table' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('myserver:dict_table_update', kwargs={'pk': dict2.pk}))
    elif 'card' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('myserver:dict_card_update', kwargs={'pk': dict2.pk}))

class DictCreateView(LoginRequiredMixin, CreateView):
    model = Dict
    form_class = DictForm

    def form_valid(self, form):
        self.object = form.save(commit=False)

        self.object.added_by = self.request.user

        word = self.object.word
        if Dict.objects.filter(word=word).count() > 0:
            if 'table' in self.request.META.get('HTTP_REFERER'):
                return redirect('myserver:dict_table_exist')
            elif 'card' in self.request.META.get('HTTP_REFERER'):
                return redirect('myserver:dict_card_exist')

        self.object.accordion_id = "accordion" + "_" + word
        self.object.heading_id = "heading" + "_" + word
        self.object.collapse_id = "collaspse" + "_" + word

        self.object.save()
        if 'table' in self.request.path:
            self.success_url = reverse_lazy('myserver:dict_detail_table', kwargs={'pk': self.object.pk})
        if 'card' in self.request.path:
            self.success_url = reverse_lazy('myserver:dict_detail_card', kwargs={'pk': self.object.pk})
        return super().form_valid(form)

@login_required
def dict_exist(request):
    return render(request, "myserver/dict_exist.html")

class DictUpdateView(LoginRequiredMixin, UpdateView):
    model = Dict
    form_class = DictForm

    def form_valid(self, form):
        self.object = form.save(commit=False)

        word = self.object.word
        self.object.word_user = word + '_' + self.request.user.username
        self.object.accordion_id = "accordion" + "_" + word
        self.object.heading_id = "heading" + "_" + word
        self.object.collapse_id = "collaspse" + "_" + word

        now = datetime.datetime.now()
        self.object.last_name_date_label = self.request.user.username + '_' + now.strftime("%Y%m%d") + ';'

        self.object.save()

        if 'table' in self.request.path:
            self.success_url = reverse_lazy('myserver:dict_detail_table', kwargs={'pk': self.object.pk})
        if 'card' in self.request.path:
            self.success_url = reverse_lazy('myserver:dict_detail_card', kwargs={'pk': self.object.pk})

        return super().form_valid(form)

class DictListView(LoginRequiredMixin, ListView):
    model = Dict
    paginate_by = 50

    total = 0
    total_today = 0

    def get_queryset(self):

        if 'table' in self.request.path:
            self.template_name = 'myserver/dict_list_table.html'
        elif 'card' in self.request.path:
            self.template_name = 'myserver/dict_list_card.html'

        # The all the user's list:
        all_list = Dict.objects.filter(Q(name_label__icontains = self.request.user.username) |
                                       Q(word_user__icontains = self.request.user.username)
        ).order_by('word')
        self.total = all_list.count()

        # For today's list of user:
        now = datetime.datetime.now()
        name_date = self.request.user.username + "_" + now.strftime("%Y%m%d")
        Q_list = [Q(last_name_date_label__icontains = name_date),
        ]
        query = reduce(operator.and_, Q_list)
        today_list = Dict.objects.filter(query).order_by('-last_date')
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
        all_list = Dict.objects.filter(Q(name_label__icontains = self.request.user.username) |
                                       Q(word_user__icontains = self.request.user.username)
                                       ).order_by('word')
        self.total = all_list.count()

        # For today's list of user:
        now = datetime.datetime.now()
        name_date = self.request.user.username + "_" + now.strftime("%Y%m%d")
        Q_list = [Q(last_name_date_label__icontains = name_date),
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

class DictDetailView(LoginRequiredMixin, DetailView):
    model = Dict

@login_required
def remove_word(request, pk):
    object = get_object_or_404(Dict, pk=pk)
    username = request.user.username
    object.remove(username)
    path = request.META.get('HTTP_REFERER')
    return redirect(path)

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
        return redirect('myserver:dict_list_table_today')
    elif 'card' in path:
        return redirect('myserver:dict_list_card_today')
