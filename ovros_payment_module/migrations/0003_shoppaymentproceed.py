# Generated by Django 4.1.4 on 2023-02-14 05:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ovros_user_module', '0006_alter_shopprofile_shop_address_no_and_more'),
        ('ovros_booking', '0002_alter_servicebooking_booking_time'),
        ('ovros_payment_module', '0002_alter_shoppaymentdetail_updated_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopPaymentProceed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_slip', models.ImageField(upload_to='users/payment')),
                ('payment_note', models.CharField(blank=True, max_length=250)),
                ('payment_booking_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ovros_booking.servicebooking')),
                ('payment_user_pro_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ovros_user_module.userprofile')),
            ],
        ),
    ]
