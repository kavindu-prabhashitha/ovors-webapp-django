# Generated by Django 4.1.4 on 2023-01-12 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ovros_service_module', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='service_description',
            field=models.CharField(default='', max_length=500),
        ),
    ]
