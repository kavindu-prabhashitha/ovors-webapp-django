from django.db import models
from ovros_user_module.models import ShopProfile, UserProfile
from ovros_booking.models import ServiceBooking


class ShopPaymentDetail(models.Model):
    shop_profile = models.OneToOneField(ShopProfile, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=100, help_text='Name of your Bank')
    bank_branch = models.CharField(max_length=50, help_text='Name of your Bank\'s branch')
    account_no = models.CharField(max_length=50, verbose_name='Account number')
    account_name = models.CharField(max_length=100, verbose_name='Account Name')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"shop : {self.shop_profile.shop_name} bank: {self.bank_name} account: {self.account_no}"


class ShopPaymentProceed(models.Model):
    payment_slip = models.ImageField(upload_to='users/payment', blank=False, )
    payment_note = models.CharField(max_length=250, blank=True)
    payment_user_pro_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    payment_booking_id = models.ForeignKey(ServiceBooking, on_delete=models.CASCADE)
