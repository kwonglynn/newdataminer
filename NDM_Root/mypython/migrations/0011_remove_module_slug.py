# Generated by Django 2.2.1 on 2019-06-08 21:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mypython', '0010_auto_20190608_2252'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='module',
            name='slug',
        ),
    ]