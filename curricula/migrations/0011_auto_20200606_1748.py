# Generated by Django 3.0.5 on 2020-06-06 17:48

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('curricula', '0010_auto_20200606_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curriculum',
            name='country',
            field=django_countries.fields.CountryField(max_length=2),
        ),
    ]