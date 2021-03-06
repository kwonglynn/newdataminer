# Generated by Django 2.2.1 on 2019-06-22 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myserver', '0010_auto_20190622_1302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dict',
            name='accordion_id',
            field=models.CharField(blank=True, default='', help_text='Format: accordion_word  Example: accordion_jag', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='dict',
            name='collapse_id',
            field=models.CharField(blank=True, default='', help_text='Format: collapse_word  Example: collapse_jag', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='dict',
            name='heading_id',
            field=models.CharField(blank=True, default='', help_text='Format: heading_word  Example: heading_jag', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='dict',
            name='last_name_date_label',
            field=models.TextField(blank=True, default='', help_text='Format: username1_date;username2_date;  Example: testuser_20190622;', null=True),
        ),
        migrations.AlterField(
            model_name='dict',
            name='name_label',
            field=models.TextField(blank=True, default='', help_text='Format: username1;username2;  Example: testuser;', null=True),
        ),
    ]
