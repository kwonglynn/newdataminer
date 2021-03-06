# Coding style for models
from django.db import models
from django.urls import reverse

# Model name should be capitalized and singular. Django admin will add an 's' to the end of the model name when it is displayed.
# Use CapWords convention (no underscores) for model name.
class University(models.Model):
    # 1. Define choices
    # Define each choice as a tuple of tuples, with an all-uppercase name.
    UNIVERSITY_TYPE = (
        ('PUB', 'A public university'),  # The key is stored in the database and should be all-uppercase. The value is the "human-readable" value for the choice field.
        ('PRI', 'A private university') # We can use get_FOO_display() to get the "human-readable" value of the choice field. FOO is the field name.
      )

    # 2. Database fields.
    # Field names should be all lowercase using underscores (snake_case) not camelCase.
    full_name = models.CharField(
        verbose_name='university full name',  # To overide the default display name of the field, which is "full name" in this case.
        max_length=100
    )
    university_type = models.CharField(
        choices=UNIVERSITY_TYPE,
        max_length=3,
        default = 'PUB',
        verbose_name='type of university',
    )

    # 3. Custom manager attributes.
    # companies = models.Manager()    # Rename the 'objects' attribute of the model, not recommended!

    # 4. The meta class
    class Meta:
        indexes = [models.Index(fields=['full_name'])]  # Adding an index for ordering can improve performance.
        ordering = ['-full_name']             # Set the default order of a list of objects. '-' means to sort decreasingly. Note that sorting can decrease preformance and should only be used when needed!.
        verbose_name = 'university'           # The model name in singular.
        verbose_name_plural = 'universities'  # The model name in plural. By default Django would just add an 's' to make it plural, namely universitys, which is wrong.

    # 5. Define __str__().
    # The __str__() method defines a human-readable representation of the model that is displayed in the Django admin site and in the Django shell.
    def __str__(self):
        return self.full_name

    # 6. Define save()
    # def save(self, *args, **kwargs):
    #    do_something()
    #    super().save(*args, **kwargs)  # Call the "real" save() method.
    #    do_something_else()

    # 7. define get_absolute_url()
    # The get_absolute_url() method sets a canonical URL for the model. This is required when using the reverse() function.
    def get_absolute_url(self):
        return reverse('university_detail', kwargs={'pk': self.id})  # 'university_detail' should be defined in the urls.py of the application.
                                                                     # kwargs corresponds to '&lt;int:pk>' in the URLconf definition.

    # 8. Custom methods.
    # def process_invoices(self):
    #    do_something()

class Student(models.Model):
    first_name = models.CharField('first name', max_length=30)  # The first positional parameter is used to overide the default display name of the field, which is "first name" in this case.
                                                                # Cannot be used for ForeignKey, ManyToManyField, or OneToOneField, becuase the first parameter is the name of another model.
    last_name = models.CharField('last name', max_length=30)
    university = models.ForeignKey(   # A ForeignKey is a key used to link two tables together. A ForeignKey is a field (or collection of fields) in one table that refers to the PRIMARY KEY in another table.
        University,                   # The table containing the foreign key is called the child table, and the table whose PRIMARY KEY is being refered to is called the referenced or parent table.
        on_delete=models.CASCADE,
        related_name='students',      # related_name should normally be the plural of the model containing the ForeignKey, default is model name in lowercase + "_set", which is "student_set" in this case.
                                      # The model inside the ForeignKey will has a special attribute in the name "related_name", here "students".
        related_query_name='person',  # related_query_name should be lowercase and singular, default is the model name in lower case, which is "student" in this case.
                                      # Examples:
                                      # yale = University.objects.get(full_name='Yale')
                                      # yale.students.all() # returns all students at Yale
                                      # yale.objects.filter(person__first_name='ashley') # returns all Yale students named Ashley
    )

    class Meta:
        verbose_name = 'student'
        verbose_name_plural = 'students'

        permissions = (("can_graduate", "Be qualified to graduate.")) # Permissions are defined in a nested tuple containing the permission name and permission display value.

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('student_detail', args=[str(self.id)])
