# Generated by Django 2.2.1 on 2019-06-02 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PythonModule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('Python', 'Python General'), ('Django', 'Django'), ('Machine', 'Machine Learning'), ('Deep', 'Deep Learning'), ('Finance', 'Finance'), ('Image', 'Image'), ('Chem', 'Cheoinformatics'), ('Bio', 'Bioinformatics')], max_length=50)),
                ('reference', models.URLField()),
                ('description', models.TextField()),
                ('submitted', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
