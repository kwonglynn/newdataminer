from django.db import models

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
    type = models.CharField(max_length=50, choices=TYPE_CHOICE)
    reference = models.URLField()
    description = models.TextField()
    submitted = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(object=self.title)
