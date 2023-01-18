from django.db import models
from ovros_user_module.models import ShopProfile, UserProfile
from ovros_service_module.models import Service

VEHICLE_TYPE = (
    ('NON', 'Non'),
    ('CAR', 'Car'),
    ('VAN', 'Van'),
    ('BIKE', 'Bike'),
    ('SUV', 'Suv')
)

BOOKING_STATUS = (
    ('PENDING', 'PENDING'),
    ('APPROVED', 'APPROVED'),
    ('CANCELED', 'CANCELED'),
)

SERVICE_STATUS = (
    ('ONGOING', 'ONGOING'),
    ('OVER', 'OVER'),
    ('FINISHED', 'FINISHED'),
)


class ServiceBooking(models.Model):
    booking_date = models.DateField()
    booking_time = models.TimeField()
    vehicle = models.CharField(choices=VEHICLE_TYPE, default='NON', max_length=5)
    booking_note = models.CharField(max_length=250, blank=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    booking_status = models.CharField(choices=BOOKING_STATUS, default='PENDING', max_length=10)

    def __str__(self):
        return f"shop {self.service.shop.shop_name}," \
               f" id {self.service.id}," \
               f" booking status {self.booking_status}"
