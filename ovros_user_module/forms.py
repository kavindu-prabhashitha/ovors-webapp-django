from django import forms
from django.contrib.auth.models import User
from .models import ShopProfile, UserProfile


USER_ROLES = [
    ('admin', 'Admin'),
    ('shop', 'Shop'),
    ('user', 'User'),
]


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('photo', 'contact_number')

    def clean(self):
        super(UserProfileEditForm, self).clean()

        contact_number = self.cleaned_data.get('contact_number')

        if not len(contact_number) == 10:
            self._errors['contact_number'] = self.error_class([
                "Contact Number Should contain 10 numbers"
            ])
        return self.cleaned_data


class ShopProfileCreationForm(forms.ModelForm):
    class Meta:
        model = ShopProfile
        fields = ('shop_name',
                  'shop_email',
                  'shop_profile_img',
                  'shop_address_no',
                  'shop_address_street',
                  'shop_address_district',
                  'shop_address_city',
                  'shop_contact')

    def clean(self):
        super(ShopProfileCreationForm, self).clean()

        contact_number = self.cleaned_data.get('shop_contact')

        if not len(contact_number) == 10:
            self._errors['shop_contact'] = self.error_class([
                "Contact Number Should contain 10 numbers"
            ])

        if not contact_number.isnumeric():
            self._errors['shop_contact'] = self.error_class([
                "Contact Number Should contain only numbers"
            ])
        return self.cleaned_data

