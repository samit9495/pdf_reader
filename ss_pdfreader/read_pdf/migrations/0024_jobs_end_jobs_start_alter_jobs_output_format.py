# Generated by Django 4.1.4 on 2023-03-06 19:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('read_pdf', '0023_alter_jobpdf_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobs',
            name='end',
            field=models.DateField(auto_now_add=True, default=datetime.datetime.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jobs',
            name='start',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='output_format',
            field=models.CharField(choices=[('JSON', 'JSON'), ('XML', 'XML'), ('CSV', 'CSV'), ('EXCEL', 'EXCEL')], max_length=50),
        ),
    ]
