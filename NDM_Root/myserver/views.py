from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

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
def index(request):
    return render(request, "myserver/index.html")

def redirect_to_list_today(request):
    if 'table' in request.META.get('HTTP_REFERER'):
        return redirect('myserver:dict_list_table_today')
    elif 'card' in request.META.get('HTTP_REFERER'):
        return redirect('myserver:dict_list_card_today')

def redirect_to_detail(request, dict):
    if 'table' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('myserver:dict_detail_table', kwargs={'pk': dict.pk}))
    elif 'card' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('myserver:dict_detail_card', kwargs={'pk': dict.pk}))

def check_exist(request, word_q):
    dicts = Dict.objects.filter(Q(word_forms__icontains=word_q))
    if dicts.exists():
        # Find the word edited by the user himself
        user_dict = dicts.filter(Q(word_user__icontains=request.user.username))

        word = word_q.split(';')[1]
        common_dict = dicts.filter(~Q(word_user__icontains=word))
        if user_dict.exists():
            dict = user_dict[0]
        # Find the common word.
        else:
            dict = common_dict[0]

        return redirect_to_detail(request, dict)

    return None

def dict_create(request):
    word_q = request.GET.get('q4', '')
    word_q = word_q.strip().lower()

    if word_q == '':
        return redirect_to_list_today(request)

    word_q = ';' + word_q + ';'  # Add ';' to help filtering.
    result = check_exist(request, word_q)
    if result:
        return result

    # assert  False

    try:
        word_in = word_q.split(';')[1].split()[0] # With scrapy, only one single word can be searched.
    except:
        # Input error.
        return redirect_to_list_today(request)

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

    os.system("conda activate django2 | scrapy crawl dict -o %s -a word=%s" % (result_file_name, word_in))
    time.sleep(1)

    while True:
        if os.path.isfile(result_file_name):
            if os.path.getsize(result_file_name) > 0:
                with open(result_file_name, 'r') as fi:
                    lines = fi.readlines()
                    result_json = lines[1].strip()
                    result_dict = json.loads(result_json)
                    word = result_dict['word']

                    try:
                        if word.endswith('*'):
                            word = word[:-1]

                        dict = Dict.objects.filter(word=word)[0]
                        if dict:
                            if ' ' in word_q:
                                word_q = word_q.split()[0] + ';'
                            if word_q not in dict.word_forms:
                                dict.add_form(word_q)

                            result = check_exist(request, word_q)  # Only for redirection here.
                            if result:
                                return result
                    except AttributeError:
                        # No word was found.
                        return redirect_to_list_today(request)
                    except IndexError:
                        # For the first search of a word!
                        pass

                    # assert False
                    word_form = ';' + word + ';'  # The root word. Add ';' to help filtering.
                    pron = result_dict['pron']
                    morf = result_dict['morf']
                    forms = result_dict['form']
                    trans_list = json.loads(result_dict['trans'])

                    # For display in table view:
                    trans_list0 = trans_list[0] # Only take the first translation for now.
                    trans = ''
                    for item in trans_list0[:2]:
                        if not re.search('[0-9]', item):
                            trans += item + ' '
                    # For display in card view and detail view:
                    trans_all = ''
                    for term in trans_list:
                        trans_all += ' '.join(term) + '<br>'

                    id = re.sub(r'\s+', '_', word)
                    accordion_id = "accordion" + "_" + id
                    heading_id = "heading" + "_" + id
                    collapse_id = "collaspse" + "_" + id

                    break
            else:
                return redirect_to_list_today(request)
        else:
            return redirect_to_list_today(request)

    dict = Dict(word=word, word_forms=word_form, pron=pron, morf=morf,
                forms=forms, trans=trans, trans_all=trans_all,
                accordion_id=accordion_id,
                heading_id=heading_id,
                collapse_id=collapse_id,
                )
    dict.added_by = request.user
    dict.save()

    ## Go back the original directory.
    os.chdir(cwd)

    return redirect_to_detail(request, dict)

@login_required
def dict_update_create(request, pk):
    dict1 = Dict.objects.filter(pk=pk)[0]

    # For the orginal word, remove the label so that it is not redundant with the new one.
    dict1.name_label = dict1.name_label.replace(request.user.username + ';', '')
    dict1.last_name_date_label = re.sub("%s_[0-9]*;" % request.user.username, "", dict1.last_name_date_label)
    dict1.save()

    dict1.pk = None
    dict2 = dict1   # Copy dict1, not necessary to give it new name, but better for clarity.

    dict2.word_user = dict2.word + '_' + request.user.username

    dict2.name_label = ''
    now = datetime.datetime.now()
    dict2.last_name_date_label = request.user.username + '_' + now.strftime("%Y%m%d") + ';'

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

        word = self.object.word.strip().lower()
        # Not allowed to add a new word, if it is already in the database.
        if Dict.objects.filter(word=word).count() > 0:
            if 'table' in self.request.META.get('HTTP_REFERER'):
                return redirect('myserver:dict_table_exist')
            elif 'card' in self.request.META.get('HTTP_REFERER'):
                return redirect('myserver:dict_card_exist')

        self.object.word = word
        self.object.word_forms = ';' + word + ';'
        id = re.sub(r'\s+', '_', word)
        self.object.accordion_id = "accordion" + "_" + id
        self.object.heading_id = "heading" + "_" + id
        self.object.collapse_id = "collaspse" + "_" + id

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

        word = self.object.word.strip().lower()
        self.object.word = word

        word_q = ';' + word + ';'
        if word_q not in self.object.word_forms:
            self.object.word_forms += ';' + word + ';'

        self.object.word_user = word + '_' + self.request.user.username

        id = re.sub(r'\s+', '_', word)
        self.object.accordion_id = "accordion" + "_" + id
        self.object.heading_id = "heading" + "_" + id
        self.object.collapse_id = "collaspse" + "_" + id

        now = datetime.datetime.now()
        self.object.last_name_date_label = self.request.user.username + '_' + now.strftime("%Y%m%d") + ';'

        self.object.save()

        if 'table' in self.request.path:
            self.success_url = reverse_lazy('myserver:dict_detail_table', kwargs={'pk': self.object.pk})
        if 'card' in self.request.path:
            self.success_url = reverse_lazy('myserver:dict_detail_card', kwargs={'pk': self.object.pk})

        return super().form_valid(form)

class DictListView(ListView):
    model = Dict
    paginate_by = 50

    total = 0
    total_today = 0

    def get_queryset(self):

        if 'table' in self.request.path:
            self.template_name = 'myserver/dict_list_table.html'
        elif 'card' in self.request.path:
            self.template_name = 'myserver/dict_list_card.html'

        # For display only if the user is not logged in.
        if not self.request.user.is_authenticated:
            self.total_today = 0
            self.total = 2

            if 'today' in self.request.path:
                # Today's word list.
                object_list = Dict.objects.none()   # Return an empty query set.
            else:
                # Total word list.
                object_list =  Dict.objects.filter((Q(word_user='') | Q(word_user=None)) & (Q(word='du') | Q(word='jag'))).order_by('word')

            return object_list

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

class DictPracticeListView(ListView):
    model = Dict
    template_name = 'myserver/dict_practice.html'
    paginate_by = 1

    total = 0
    total_today = 0

    def get_queryset(self):

        # For display only if the user is not logged in.
        if not self.request.user.is_authenticated:
            self.total_today = 0
            self.total = 2

            if 'today' in self.request.path:
                # Today's word list.
                object_list = Dict.objects.none()   # Return an empty query set.
            else:
                # Total word list.
                object_list =  Dict.objects.filter((Q(word_user='') | Q(word_user=None)) & (Q(word='du') | Q(word='jag'))).order_by('word')

            return object_list

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

class DictDetailView(DetailView):
    model = Dict

@login_required
def remove_word(request, pk):
    object = get_object_or_404(Dict, pk=pk)
    username = request.user.username
    if object.word_user and (username in object.word_user):
        object.delete()
    else:
        object.remove(username)
    path = request.META.get('HTTP_REFERER')
    return redirect(path)

@login_required
def remember_word(request, pk):
    object = get_object_or_404(Dict, pk=pk)
    username = request.user.username
    if object.word_user and (username in object.word_user):
        object.delete()
    else:
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
    else:
        # For 'card' view and other occasions.
        return redirect('myserver:dict_list_card_today')
