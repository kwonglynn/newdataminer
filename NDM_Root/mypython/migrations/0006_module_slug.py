# Generated by Django 2.2.1 on 2019-06-02 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mypython', '0005_auto_20190602_2126'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='slug',
            field=models.SlugField(default=''),
        ),
    ]
