# Generated by Django 2.2.1 on 2019-06-18 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deep', '0002_auto_20190612_1724'),
    ]

    operations = [
        migrations.AddField(
            model_name='deep',
            name='usage',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
