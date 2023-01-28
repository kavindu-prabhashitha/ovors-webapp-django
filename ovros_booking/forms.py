from django import forms
from .models import ServiceBooking


class BookingCreationForm(forms.ModelForm):
    class Meta:
        model = ServiceBooking
        fields = (
            'vehicle',
            'booking_date',
            'booking_time',
            'booking_note',
        )

        widgets = {
            'booking_note': forms.Textarea(attrs={
                'rows': 4, 'cols': 15
            }),

            'booking_date': forms.DateInput(format=('%d/%m/%Y'),
                                            attrs={'class': 'form-control',
                                                   'placeholder': 'Select a date',
                                                   'type': 'date'
                                                   # <--- IF I REMOVE THIS LINE, THE INITIAL VALUE IS DISPLAYED
                                                   }),
            'booking_time': forms.TimeInput(
               attrs={
                   'class': 'form-control',
                   'type': 'time'
               }
            ),
        }


class BookingStatusChangeForm(forms.ModelForm):
    class Meta:
        model = ServiceBooking
        fields = ('booking_status',)


class ServiceStatusChangeForm(forms.ModelForm):
    class Meta:
        model = ServiceBooking
        fields = ('service_status', )


class ServicePaymentStatusChangeForm(forms.ModelForm):
    class Meta:
        model=ServiceBooking
        fields = ('payment_status', )

