# Generated by Django 2.2.1 on 2019-06-17 09:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myserver', '0003_remove_dict_phrase'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dict',
            old_name='form',
            new_name='forms',
        ),
    ]
