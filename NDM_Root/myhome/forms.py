# Contact Form
from django import forms

class ContactForm(forms.Form):
    yourname = forms.CharField(max_length=100, label='Name')
    email = forms.EmailField(required=False, label='Email')
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)

# User Create Form
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ("username", "email", "password1", "password2")
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Username"
        self.fields["email"].label = "Email address"
