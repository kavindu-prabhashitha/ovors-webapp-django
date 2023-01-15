from django.db import models
from django.conf import settings


class Types(models.TextChoices):
    USER_ADMIN = "USER_ADMIN", "UserAdmin"
    USER_SHOP = "USER_SHOP", "UserShop"
    USER_SHOP_MEMBER = "USER_SHOP_MEMBER", "UserShopMember"
    USER_CUSTOMER = "USER_CUSTOMER", "UserCustomer"


# class Profile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     date_of_birth = models.DateField(blank=True, null=True)
#     photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)
#
#     def __str__(self):
#         return f'Profile for user {self.user.username}'


class ShopProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_role = models.CharField('Type', max_length=40, choices=Types.choices, default=Types.USER_SHOP)
    shop_name = models.CharField(max_length=100, help_text="Service Shop name")
    shop_address = models.CharField(max_length=200, help_text="Service Shop address")
    shop_contact = models.CharField(max_length=20)

    def __str__(self):
        return f'Shop Profile for {self.shop_name}'


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_role = models.CharField('Type', max_length=40, choices=Types.choices, default=Types.USER_CUSTOMER)
    photo = models.ImageField(upload_to='users/%Y', blank=True,)
    contact_number = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_created=True, null=True)

    def __str__(self):
        return f'Profile for user {self.user.username}'


class UserBankDetails(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=100, help_text='Name of your Bank')
    bank_account_no = models.CharField(max_length=50)
    bank_branch = models.CharField(max_length=50)
    bank_account_name = models.CharField(max_length=100)

    def __str__(self):
        return f'Bank Account in {self.bank_name} account number is {self.bank_account_no}'


