# Generated by Django 2.2.1 on 2019-06-19 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mypython', '0018_module_usage'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='script',
            field=models.FileField(blank=True, null=True, upload_to='deep/%Y/%m/%d/'),
        ),
    ]
