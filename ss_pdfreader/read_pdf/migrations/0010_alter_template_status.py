# Generated by Django 4.1.4 on 2023-01-11 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('read_pdf', '0009_template_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='status',
            field=models.CharField(choices=[('Sent for Approval', 'Sent for Approval'), ('Approved', 'Approved'), ('Draft', 'Draft')], max_length=500),
        ),
    ]
