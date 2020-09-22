# Generated by Django 3.0.5 on 2020-04-28 21:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('analyses', '0005_auto_20200428_1127'),
    ]

    operations = [
        migrations.RenameField(
            model_name='learningoutcomecategoryhitcount',
            old_name='title',
            new_name='category',
        ),
        migrations.CreateModel(
            name='StrandCategoryOccurrence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('occurrences', models.PositiveIntegerField(default=0)),
                ('strand_analysis', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='strand_category_occurrences', to='analyses.StrandAnalysis')),
            ],
        ),
    ]
