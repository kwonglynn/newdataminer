# Generated by Django 2.2.1 on 2019-06-12 14:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mypython', '0015_auto_20190610_1943'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='module',
            options={'permissions': (('can_publish_module', 'Can publish and delete modules.'),), 'verbose_name_plural': 'Python modules'},
        ),
    ]
