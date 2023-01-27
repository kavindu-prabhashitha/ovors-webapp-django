from django.db import models
from ovros_user_module.models import ShopProfile


class ShopPaymentDetail(models.Model):
    shop_profile = models.OneToOneField(ShopProfile, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=100, help_text='Name of your Bank')
    bank_branch = models.CharField(max_length=50, help_text='Name of your Bank\'s branch')
    account_no = models.CharField(max_length=50, verbose_name='Account number')
    account_name = models.CharField(max_length=100, verbose_name='Account Name')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(blank=True)

    def __str__(self):
        return f"shop : {self.shop_profile.shop_name} bank: {self.bank_name} account: {self.account_no}"
