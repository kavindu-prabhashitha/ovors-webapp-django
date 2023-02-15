from django import forms
from .models import ShopPaymentDetail, ShopPaymentProceed


class ShopBankDetAddForm(forms.ModelForm):
    class Meta:
        model = ShopPaymentDetail
        fields = ('bank_name', 'bank_branch', 'account_no', 'account_name')


class ShopBankDetEditForm(forms.ModelForm):
    class Meta:
        model = ShopPaymentDetail
        fields = ('bank_name', 'bank_branch', 'account_no', 'account_name')


class PaymentProceedForm(forms.ModelForm):
    class Meta:
        model = ShopPaymentProceed
        fields = ('payment_slip', 'payment_note')

        widgets = {
            'payment_note': forms.Textarea(attrs={
                "rows": 5, "cols": 20
            })
        }


