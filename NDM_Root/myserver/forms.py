from django import forms
from django.forms import ModelForm
from .models import Dict
from django.utils.translation import ugettext_lazy as _

class DictForm(ModelForm):
    class Meta:
        model = Dict
        fields = ['word', 'pron', 'morf', 'forms', 'trans', 'trans_all']
