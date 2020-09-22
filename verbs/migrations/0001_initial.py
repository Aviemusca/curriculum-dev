# Generated by Django 3.0.5 on 2020-09-21 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('analyses', '0019_auto_20200522_2239'),
        ('verb_categories', '0005_auto_20200603_1324'),
    ]

    operations = [
        migrations.CreateModel(
            name='Verb',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(blank=True, max_length=150, unique=True)),
                ('verb_categories', models.ManyToManyField(related_name='verbs', to='verb_categories.VerbCategory')),
            ],
            options={
                'verbose_name': 'Verb',
                'verbose_name_plural': 'Verbs',
            },
        ),
        migrations.CreateModel(
            name='NonVerb',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(blank=True, max_length=150, unique=True)),
                ('verb_categories', models.ManyToManyField(related_name='non_verbs', to='verb_categories.VerbCategory')),
            ],
            options={
                'verbose_name': 'Non Verb',
                'verbose_name_plural': 'Non Verbs',
            },
        ),
        migrations.CreateModel(
            name='NonCatVerb',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(blank=True, max_length=150, unique=True)),
                ('curriculum_analyses', models.ManyToManyField(related_name='non_cat_verbs', to='analyses.CurriculumAnalysis')),
            ],
            options={
                'verbose_name': 'Non Categorised Verb',
                'verbose_name_plural': 'Non Categorised Verbs',
            },
        ),
    ]
