from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.core.mail import send_mail
from django.conf import settings
from django.template import loader
from .forms import ContactForm
import re
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives

from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

# Create your views here.
def index(request):
    return render(request, "myhome/index.html")

def textify(html):
    # Remove html tags and continuous whitespaces
    text_only = re.sub('[ \t]+', ' ', strip_tags(html))
    # Strip single spaces in the beginning of each line
    return text_only.replace('\n ', '\n').strip()

def contact(request):
    submitted = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            subject = cd['subject']
            sender = cd['yourname']
            email = cd.get('email', '')
            message = cd['message']
            from_email = settings.EMAIL_HOST_USER
            recipient_list = ['guanglin@kth.se',]

            email_context = {
                                'subject': subject,
                                'sender': sender,
                                'email': email,
                                'message': message
                            }

            html_message = loader.render_to_string(
                            'myhome/email.html',
                            email_context)

            text_message = textify(html_message)

            msg = EmailMultiAlternatives(subject=subject,
                                         body=text_message,
                                         from_email=from_email,
                                         to=recipient_list,
                                         )
            msg.attach_alternative(html_message, "text/html")
            # assert False
            msg.send()

            # send_mail(subject=subject,
            #           message=text_message,
            #           from_email=from_email,
            #           recipient_list=recipient_list,
            #           fail_silently=True,
            #           html_message=html_message)

            return HttpResponseRedirect('/contact?submitted=True')
    else:
        form = ContactForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'myhome/contact.html', {'form': form, 'submitted': submitted})

# User registration
def register_success(request):
    return render(request, "registration/success.html")


# Create your views here.
class Register(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('myhome:register-success')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)
