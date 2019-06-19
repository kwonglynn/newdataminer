from django import forms
from django.forms import ModelForm
from .models import Machine
from django.utils.translation import ugettext_lazy as _

class MachineForm(ModelForm):
    class Meta:
        model = Machine
        fields = ['title', 'usage', 'reference', 'description', 'parameters', 'code', 'script']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
            'parameters': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
            'code': forms.Textarea(attrs={'class': 'codecontent'})
        }
