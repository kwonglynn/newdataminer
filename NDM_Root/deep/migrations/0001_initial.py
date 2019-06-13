# Generated by Django 2.2.1 on 2019-06-12 14:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('reference', models.URLField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('parameters', models.TextField(blank=True, null=True)),
                ('code', models.TextField(blank=True, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('added_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deep', to=settings.AUTH_USER_MODEL, verbose_name='Added by')),
            ],
            options={
                'verbose_name_plural': 'Deep Learning',
                'permissions': (('can_publish_module', 'Can publish and delete modules.'),),
            },
        ),
    ]
