# Generated by Django 3.0.5 on 2020-06-10 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curricula', '0011_auto_20200606_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curriculum',
            name='public',
            field=models.BooleanField(default=False),
        ),
    ]
