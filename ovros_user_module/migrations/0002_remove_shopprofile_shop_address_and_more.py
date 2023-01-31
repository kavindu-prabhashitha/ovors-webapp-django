# Generated by Django 4.1.4 on 2023-01-29 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ovros_user_module', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shopprofile',
            name='shop_address',
        ),
        migrations.AddField(
            model_name='shopprofile',
            name='shop_address_city',
            field=models.CharField(default=9999, help_text='Service Shop address city', max_length=200),
        ),
        migrations.AddField(
            model_name='shopprofile',
            name='shop_address_district',
            field=models.CharField(default=9999, help_text='Service Shop address district', max_length=200),
        ),
        migrations.AddField(
            model_name='shopprofile',
            name='shop_address_no',
            field=models.CharField(default=9999, help_text='Service Shop address Number', max_length=200),
        ),
        migrations.AddField(
            model_name='shopprofile',
            name='shop_address_street',
            field=models.CharField(default=9999, help_text='Service Shop address street', max_length=200),
        ),
        migrations.AlterField(
            model_name='shopprofile',
            name='shop_contact',
            field=models.CharField(max_length=10),
        ),
    ]
