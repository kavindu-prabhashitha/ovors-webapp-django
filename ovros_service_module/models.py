from django.db import models
from ovros_user_module.models import ShopProfile
import os
# Create your models here.

SERVICE_AVAILABILITY = (
    ('available', 'Available'),
    ('unavailable', 'Unavailable'),
)


class Service(models.Model):
    shop = models.ForeignKey(to=ShopProfile, on_delete=models.CASCADE)
    service_name = models.CharField(max_length=100)
    service_image = models.ImageField(upload_to='images/service_img', blank=True)
    service_description = models.CharField(max_length=500, default='', blank=True)
    service_price = models.DecimalField(max_digits=10, decimal_places=2)
    service_duration = models.CharField(max_length=5)
    is_for_car = models.BooleanField(verbose_name="Available for car", default=False)
    is_for_van = models.BooleanField(verbose_name="Available for van", default=False)
    is_for_suv = models.BooleanField(verbose_name="Available for suv", default=False)
    is_for_lorry = models.BooleanField(verbose_name="Available for lorry", default=False)
    is_for_bike = models.BooleanField(verbose_name="Available for bike", default=False)
    service_availability = models.BooleanField(
        verbose_name="Service availability",
        default=False,
        help_text="is service available currently"
    )
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    def __str__(self):
        return f"Servie Name : {self.service_name} is available : {self.service_availability}"


class ServicePart(models.Model):
    part_name = models.CharField(max_length=50)
    part_type = models.CharField(max_length=50)
    part_price = models.DecimalField(max_digits=10, decimal_places=2)
    service = models.ManyToManyField(Service, through='PartForService')

    def __str__(self):
        return f"S_Part Name : {self.part_name}"


class PartForService(models.Model):
    servie = models.ForeignKey(Service, on_delete=models.CASCADE)
    service_part = models.ForeignKey(ServicePart, on_delete=models.CASCADE)
    date_added = models.DateField()
    date_updated = models.DateField(blank=True, null=True)



