# Generated by Django 3.0.5 on 2020-06-11 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomies', '0008_customusertaxonomy_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='customusertaxonomy',
            name='public',
            field=models.BooleanField(default=False),
        ),
    ]