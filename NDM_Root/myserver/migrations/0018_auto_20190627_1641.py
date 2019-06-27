# Generated by Django 2.2.1 on 2019-06-27 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myserver', '0017_remove_dict_added_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dict',
            name='last_name_date_label',
            field=models.TextField(blank=True, default=';', help_text='Format: username1_date;username2_date; &nbsp;&nbsp;&nbsp;Example: testuser_20190622;', null=True),
        ),
        migrations.AlterField(
            model_name='dict',
            name='name_label',
            field=models.TextField(blank=True, default=';', help_text='Format: username1;username2; &nbsp;&nbsp;&nbsp;Example: testuser;', null=True),
        ),
        migrations.AlterField(
            model_name='dict',
            name='word_forms',
            field=models.CharField(blank=True, default=';', max_length=200, null=True),
        ),
    ]
