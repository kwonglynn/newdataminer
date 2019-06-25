from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
import re

# Create your models here.

class Dict(models.Model):
    word = models.CharField(max_length=200)
    word_forms = models.CharField(max_length=200, blank=True, null=True, default='') # To store different forms of the word for search efficiency.
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Added by", related_name='dict')
    word_user = models.CharField(max_length=200, blank=True, null=True, default='')

    pron = models.CharField(max_length=100, blank=True, null=True, default='')
    morf = models.CharField(max_length=100, blank=True, null=True, default='')
    forms = models.CharField(max_length=100, blank=True, null=True, default='')
    trans = models.TextField(blank=True, null=True, help_text='For concise display in table view.')
    trans_all = models.TextField(blank=True, null=True, default='', help_text='For more detailed display in card view and detail view.')
    # phrase = models.TextField(blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    last_date = models.DateTimeField(auto_now=True)

    name_label = models.TextField(blank=True, null=True, default='', help_text='Format: username1;username2; &nbsp;&nbsp;&nbsp;Example: testuser;')
    last_name_date_label = models.TextField(blank=True, null=True, default='', help_text='Format: username1_date;username2_date; &nbsp;&nbsp;&nbsp;Example: testuser_20190622;')

    accordion_id = models.CharField(max_length=200, blank=True, null=True, default='', help_text="Format: accordion_word &nbsp;&nbsp;&nbsp;Example: accordion_jag")
    heading_id = models.CharField(max_length=200, blank=True, null=True, default='', help_text="Format: heading_word &nbsp;&nbsp;&nbsp;Example: heading_jag")
    collapse_id = models.CharField(max_length=200, blank=True, null=True, default='', help_text="Format: collapse_word &nbsp;&nbsp;&nbsp;Example: collapse_jag")

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

    def add_form(self, word_q):
        self.word_forms += word_q
        self.save()
