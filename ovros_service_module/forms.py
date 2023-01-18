from django import forms
from .models import Service,ServicePart,PartForService


class ServiceCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Service
        fields = ('service_name', 'service_image', 'service_description', 'service_duration', 'service_price', 'date_created')
        widgets = {
            'date_created': forms.DateInput(format=('%d/%m/%Y'),
                                            attrs={'class': 'form-control',
                                                   'placeholder': 'Select a date',
                                                   'type': 'date'
                                                   # <--- IF I REMOVE THIS LINE, THE INITIAL VALUE IS DISPLAYED
                                                   }),

            'service_description': forms.Textarea(attrs={
                "rows": 5, "cols": 20
            })
        }


class ServiceEditForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = (
            'service_name',
            'service_image',
            'service_description',
            'service_duration',
            'service_price',
        )

        widgets = {
            'date_created': forms.DateInput(format=('%d/%m/%Y'),
                                            attrs={'class': 'form-control',
                                                   'placeholder': 'Select a date',
                                                   'type': 'date'
                                                   # <--- IF I REMOVE THIS LINE, THE INITIAL VALUE IS DISPLAYED
                                                   }),

            'service_description': forms.Textarea(attrs={
                "rows": 5, "cols": 20
            })
        }
