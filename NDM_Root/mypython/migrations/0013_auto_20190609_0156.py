# Generated by Django 2.2.1 on 2019-06-08 23:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mypython', '0012_auto_20190608_2336'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='module',
            options={'permissions': (('can_publish_module', 'Can publish and delete modules.'),)},
        ),
    ]
