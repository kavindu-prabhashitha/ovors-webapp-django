from django import forms
from common.enums import VEHICLE_TYPE, DISTRICTS


class ServiceSearchForm(forms.Form):
    search_by_district = forms.ChoiceField(choices=DISTRICTS, required=False)
    search_by_city = forms.ChoiceField(required=False)
    search_by_vehicle = forms.ChoiceField(required=False, choices=VEHICLE_TYPE, initial=VEHICLE_TYPE[0])
    search_by_Keyword = forms.CharField(required=False, max_length=50)


class ServiceSearchForm01(forms.Form):
    search_by_district = forms.ChoiceField(choices=DISTRICTS, required=False)
    search_by_city = forms.ChoiceField(required=False, help_text="first select a district")


class ServiceSearchForm02(forms.Form):
    search_by_vehicle = forms.ChoiceField(required=False, choices=VEHICLE_TYPE, initial=VEHICLE_TYPE[0])
    search_by_Keyword = forms.CharField(required=False, max_length=50)
