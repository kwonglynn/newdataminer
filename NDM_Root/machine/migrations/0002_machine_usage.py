# Generated by Django 2.2.1 on 2019-06-18 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('machine', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='machine',
            name='usage',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
