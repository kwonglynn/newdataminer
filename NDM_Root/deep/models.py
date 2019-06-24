from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Deep(models.Model):
    title = models.CharField(max_length=100)
    usage = models.CharField(max_length=300, blank=True, null=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Added by", related_name='deep')
    reference = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    parameters = models.TextField(blank=True, null=True)
    code = models.TextField(blank=True, null=True)
    script = models.FileField(upload_to="deep/%Y/%m/%d/", blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        permissions = (("can_publish_delete", "Can publish and delete modules."),)
        verbose_name_plural = "Deep Learning"

    def __str__(self):
        return str(object=self.title)

    def get_absolute_url(self):
        return reverse("deep:deep_detail", kwargs={'pk':self.pk}) # Remember to use the app name as prefix for reverse!

    def publish(self):
        self.published_date = timezone.now()
        self.save()
