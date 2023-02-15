from django.db import models
from common.enums import SHOP_REPORT_TYPES, USER_REPORT_TYPES
# Create your models here.


class ShopReport(models.Model):
    name = models.CharField(max_length=100)
    report_type = models.CharField(choices=SHOP_REPORT_TYPES, max_length=40)
    from_date = models.DateField()
    to_date = models.DateField()
    created_at = models.DateField(auto_now_add=True)


class UserReport(models.Model):
    name = models.CharField(max_length=100)
    report_type = models.CharField(choices=USER_REPORT_TYPES, max_length=40)
    from_date = models.DateField()
    to_date = models.DateField()
    created_at = models.DateField(auto_now_add=True)
