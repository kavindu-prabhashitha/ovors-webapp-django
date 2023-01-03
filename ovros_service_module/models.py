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
    service_price = models.CharField(max_length=20)
    service_duration = models.CharField(max_length=5)
    date_created = models.DateField()

    def __str__(self):
        return f"Servie Name : {self.service_name}"


class ServicePart(models.Model):
    part_name = models.CharField(max_length=50)
    part_type = models.CharField(max_length=50)
    part_price = models.CharField(max_length=20)
    service = models.ManyToManyField(Service, through='PartForService')

    def __str__(self):
        return f"S_Part Name : {self.part_name}"


class PartForService(models.Model):
    servie = models.ForeignKey(Service, on_delete=models.CASCADE)
    service_part = models.ForeignKey(ServicePart, on_delete=models.CASCADE)
    date_added = models.DateField()
    date_updated = models.DateField(blank=True, null=True)



