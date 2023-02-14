from django import forms
from .models import ShopReport, UserReport
import datetime


class ShopReportGenerateForm(forms.ModelForm):
    class Meta:
        model = ShopReport
        fields = ('name', "from_date", 'to_date', 'report_type', )
        widgets = {
            'from_date': forms.DateInput(format=('%d/%m/%Y'),
                                            attrs={'class': 'form-control',
                                                   'placeholder': 'Select a date',
                                                   'type': 'date'
                                                   }),

            'to_date': forms.DateInput(format=('%d/%m/%Y'),
                                         attrs={'class': 'form-control',
                                                'placeholder': 'Select a date',
                                                'type': 'date'
                                                }),
        }

    def clean(self):
        super(ShopReportGenerateForm, self).clean()
        from_date = self.cleaned_data.get('from_date')
        to_date = self.cleaned_data.get('to_date')

        if to_date > datetime.date.today():
            self._errors['to_date'] = self.error_class([
                "The date cannot be in the Future!"
            ])

        if from_date > datetime.date.today():
            self._errors['from_date'] = self.error_class([
                "The date cannot be in the Past!"
            ])
        return self.cleaned_data


class UserReportGenerateForm(forms.ModelForm):
    class Meta:
        model = UserReport
        fields = ('name', "from_date", 'to_date', 'report_type', )
        widgets = {
            'from_date': forms.DateInput(format=('%d/%m/%Y'),
                                            attrs={'class': 'form-control',
                                                   'placeholder': 'Select a date',
                                                   'type': 'date'
                                                   }),

            'to_date': forms.DateInput(format=('%d/%m/%Y'),
                                         attrs={'class': 'form-control',
                                                'placeholder': 'Select a date',
                                                'type': 'date'
                                                }),
        }
