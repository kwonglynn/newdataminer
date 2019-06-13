from django import forms
from django.forms import ModelForm
from .models import Module
from django.utils.translation import ugettext_lazy as _

class ModuleForm(ModelForm):
    # required_css_class = 'required'
    class Meta:
        model = Module
        # fields = '__all__'
        fields = ['title', 'type', 'reference', 'description', 'code']
        # labels = {'type': 'Module Type'}
        # help_texts = {'reference': _('Input the link for the module.')}
        widgets = {
            'description': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
            'code': forms.Textarea(attrs={'class': 'codecontent'})
        }
