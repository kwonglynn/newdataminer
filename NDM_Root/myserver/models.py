from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
import re

# Create your models here.

class Dict(models.Model):
    word = models.CharField(max_length=100)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Added by", related_name='dict')
    pron = models.CharField(max_length=100, blank=True, null=True)
    morf = models.CharField(max_length=100, blank=True, null=True)
    forms = models.CharField(max_length=100, blank=True, null=True, default='')
    trans = models.TextField(blank=True, null=True)
    # phrase = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_date = models.DateTimeField(auto_now=True)
    name_label = models.TextField(blank=True, null=True, default='')
    last_name_date_label = models.TextField(blank=True, null=True, default='')

    accordion_id = models.CharField(max_length=200, blank=True, null=True)
    heading_id = models.CharField(max_length=200, blank=True, null=True)
    collapse_id = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return str(object=self.word)

    def get_absolute_url(self):
        return reverse("myserver:dict_detail", kwargs={'pk':self.pk}) # Remember to use the app name as prefix for reverse!

    def add(self, username):
        self.name_label += username + ';'
        now = datetime.datetime.now()
        self.last_name_date_label += username + '_' + now.strftime("%Y%m%d") + ';'
        self.save()

    def remove(self, username):
        self.name_label = self.name_label.replace(username + ';', '')
        self.last_name_date_label = re.sub("%s_[0-9]*;" % username, "", self.last_name_date_label)
        self.save()
