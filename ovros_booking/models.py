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
    ('PENDING', 'PENDING'),
    ('QUEUED', 'QUEUED'),
    ('ONGOING', 'ONGOING'),
    ('OVER', 'OVER'),
)

PAYMENT_STATUS = (
    ('PAYMENT_PENDING', 'PAYMENT_PENDING'),
    ('PAYMENT_PROCESSING', 'PAYMENT_PROCESSING'),
    ('PAYMENT_COMPLETED', 'PAYMENT_COMPLETED'),
)


class ServiceBooking(models.Model):
    booking_date = models.DateField()
    booking_time = models.TimeField(null=True)
    vehicle = models.CharField(choices=VEHICLE_TYPE, default='NON', max_length=5)
    booking_note = models.CharField(max_length=250, blank=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    booking_status = models.CharField(choices=BOOKING_STATUS, default='PENDING', max_length=10)
    service_status = models.CharField(choices=SERVICE_STATUS, default='PENDING', max_length=30)
    payment_status = models.CharField(choices=PAYMENT_STATUS, default='PAYMENT_PENDING', max_length=30)

    def __str__(self):
        return f"shop {self.service.shop.shop_name}," \
               f" id {self.service.id}," \
               f" booking status {self.booking_status}"\
               f" service status {self.service_status}"
