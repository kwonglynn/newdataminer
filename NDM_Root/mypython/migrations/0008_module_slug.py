# Generated by Django 2.2.1 on 2019-06-02 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mypython', '0007_remove_module_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='slug',
            field=models.SlugField(default=''),
        ),
    ]
