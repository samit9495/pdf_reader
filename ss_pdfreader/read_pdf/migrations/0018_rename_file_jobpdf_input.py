# Generated by Django 4.1.4 on 2023-03-01 18:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('read_pdf', '0017_remove_jobs_input'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jobpdf',
            old_name='file',
            new_name='input',
        ),
    ]
