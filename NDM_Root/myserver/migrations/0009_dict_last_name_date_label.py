# Generated by Django 2.2.1 on 2019-06-22 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myserver', '0008_auto_20190621_0044'),
    ]

    operations = [
        migrations.AddField(
            model_name='dict',
            name='last_name_date_label',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
