from django import forms
from common.enums import VEHICLE_TYPE,DISTRICTS


class ServiceSearchForm(forms.Form):
    search_by_district = forms.ChoiceField(choices=DISTRICTS, required=False)
    search_by_city = forms.ChoiceField(required=False)
    search_by_vehicle = forms.ChoiceField(required=False, choices=VEHICLE_TYPE, initial=VEHICLE_TYPE[1])
    search_by_Keyword = forms.CharField(required=False, max_length=50)
