from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Dict(models.Model):
    word = models.CharField(max_length=100)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Added by", related_name='dict')
    pron = models.CharField(max_length=100, blank=True, null=True)
    morf = models.CharField(max_length=100, blank=True, null=True)
    forms = models.CharField(max_length=100, blank=True, null=True, default='')
    trans = models.TextField(blank=True, null=True)
    # phrase = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    label = models.TextField(blank=True, null=True, default='')

    def __str__(self):
        return str(object=self.word)

    def get_absolute_url(self):
        return reverse("myserver:dict_detail", kwargs={'pk':self.pk}) # Remember to use the app name as prefix for reverse!

    def add(self, username):
        self.label += username + ';'
        self.save()

    def remove(self, username):
        self.label = self.label.replace(username + ';', '')
        self.save()
