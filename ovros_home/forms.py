from django import forms
from common.enums import VEHICLE_TYPE, DISTRICTS, DISTRICTS_CITY


class ServiceSearchForm(forms.Form):
    search_by_district = forms.ChoiceField(required=False, choices=DISTRICTS, initial=DISTRICTS[1])
    search_by_city = forms.ChoiceField(required=False, choices=DISTRICTS_CITY)
    search_by_vehicle = forms.ChoiceField(required=False, choices=VEHICLE_TYPE, initial=VEHICLE_TYPE[0])
    search_by_service = forms.CharField(required=False, max_length=50)


class ServiceSearchForm01(forms.Form):
    search_by_district = forms.ChoiceField(choices=DISTRICTS, required=False, initial=DISTRICTS[1])
    search_by_city = forms.ChoiceField(required=False, help_text="first select a district", choices=DISTRICTS_CITY)


class ServiceSearchForm02(forms.Form):
    search_by_vehicle = forms.ChoiceField(required=False, choices=VEHICLE_TYPE, initial=VEHICLE_TYPE[0])
    search_by_service = forms.CharField(required=False, max_length=50)


class ServiceSearchByShop(forms.Form):
    search_by_shop = forms.CharField(label="Search by Shop Name", required=False, max_length=100,)
