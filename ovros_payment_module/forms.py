from django import forms
from .models import ShopPaymentDetail


class ShopBankDetAddForm(forms.ModelForm):
    class Meta:
        model = ShopPaymentDetail
        fields = ('bank_name', 'bank_branch', 'account_no', 'account_name')


class ShopBankDetEditForm(forms.ModelForm):
    class Meta:
        model = ShopPaymentDetail
        fields = ('bank_name', 'bank_branch', 'account_no', 'account_name')

