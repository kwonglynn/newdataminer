# Generated by Django 2.2.1 on 2019-06-19 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deep', '0003_deep_usage'),
    ]

    operations = [
        migrations.AddField(
            model_name='deep',
            name='script',
            field=models.FileField(blank=True, null=True, upload_to='deep'),
        ),
    ]
