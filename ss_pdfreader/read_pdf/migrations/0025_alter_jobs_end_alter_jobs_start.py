# Generated by Django 4.1.4 on 2023-03-06 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('read_pdf', '0024_jobs_end_jobs_start_alter_jobs_output_format'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobs',
            name='end',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='start',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
