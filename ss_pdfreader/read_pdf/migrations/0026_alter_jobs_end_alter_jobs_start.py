# Generated by Django 4.1.4 on 2023-03-06 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('read_pdf', '0025_alter_jobs_end_alter_jobs_start'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobs',
            name='end',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='start',
            field=models.DateTimeField(),
        ),
    ]
