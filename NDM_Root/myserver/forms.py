from django import forms
from django.forms import ModelForm
from .models import Dict
from django.utils.translation import ugettext_lazy as _

# class DictForm(ModelForm):
#     class Meta:
#         model = Dict
#         fields = ['title', 'reference', 'description', 'parameters', 'code']
#         widgets = {
#             'description': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
#             'parameters': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
#             'code': forms.Textarea(attrs={'class': 'codecontent'})
#         }
