# Generated by Django 2.2.1 on 2019-06-28 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mypython', '0021_auto_20190628_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='type',
            field=models.CharField(choices=[('Bash', 'Bash'), ('Python', 'Python'), ('Django', 'Django'), ('Machine', 'Machine Learning'), ('Deep', 'Deep Learning'), ('Finance', 'Finance'), ('Image', 'Image'), ('Chem', 'Cheoinformatics'), ('Bio', 'Bioinformatics')], max_length=10),
        ),
    ]
