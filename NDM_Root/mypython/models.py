from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

TYPE_CHOICE = (
    ('Python', 'Python General'),
    ('Django', 'Django'),
    ('Machine', 'Machine Learning'),
    ('Deep', 'Deep Learning'),
    ('Finance', 'Finance'),
    ('Image', 'Image'),
    ('Chem', 'Cheoinformatics'),
    ('Bio', 'Bioinformatics')
)

# Note that Django will add an 's' to end of the module name in the admin page!
# Think carefully for the module name and field names.
# It would be painful to change them after they have already been created!
class Module(models.Model):
    title = models.CharField(max_length=100)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Added by", related_name='python')
    type = models.CharField(max_length=10, choices=TYPE_CHOICE)
    usage = models.CharField(max_length=300, blank=True, null=True)
    reference = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    code = models.TextField(blank=True, null=True)
    script = models.FileField(upload_to="mypython/%Y/%m/%d/", blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        permissions = (("can_publish_module", "Can publish and delete modules."),)
        verbose_name_plural = "Python modules"

    def __str__(self):
        return str(object=self.title)

    def get_absolute_url(self):
        return reverse("mypython:module_detail", kwargs={'pk':self.pk}) # Remember to use the app name as prefix for reverse!

    def publish(self):
        self.published_date = timezone.now()
        self.save()
