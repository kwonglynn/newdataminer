from django import forms
from django.forms import ModelForm
from .models import Module

class ModuleForm(ModelForm):
    required_css_class = 'required'
    class Meta:
        model = Module
        fields = ['title', 'type', 'reference', 'description']
