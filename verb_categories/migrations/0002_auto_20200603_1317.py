# Generated by Django 3.0.5 on 2020-06-03 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verb_categories', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verbcategory',
            name='level',
            field=models.PositiveIntegerField(default=1, unique=True),
        ),
    ]
