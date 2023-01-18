from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import BookingCreationForm
from .models import ServiceBooking
from ovros_service_module.models import Service
from ovros_user_module.models import UserProfile
from django.contrib import messages
# Create your views here.


@login_required
def add_booking(request, service_id):
    user_profile_id = request.session['profile_data']['profile_data']['profile_id']
    if request.method == 'POST':
        form = BookingCreationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            service = get_object_or_404(Service, id=service_id)
            user = get_object_or_404(UserProfile, id=user_profile_id)
            service_booking = ServiceBooking()
            service_booking.service = service
            service_booking.user = user
            service_booking.booking_date = cd['booking_date']
            service_booking.booking_time = cd['booking_time']
            service_booking.booking_note = cd['booking_note']
            service_booking.vehicle = cd['vehicle']
            booked_service = service_booking.save()
            print(f'profile id : {user_profile_id}, booking_id : {booked_service}')
            messages.success(request, "Booking Added Successfully , status : PENDING")
            return render(request,
                          'ovros_dashboard/user_dashboard/user_dashboard_overview.html',
                          {'section': 'dashboard'}
                          )
    else:
        service = Service.objects.get(id=service_id)
        booking_form = BookingCreationForm()
        return render(request,
                      'ovros_dashboard/user_dashboard/user_dashboard_bookings_add.html',
                      {'form': booking_form,
                       'section':'dashboard',
                       'service': service}
                      )


@login_required
def view_user_bookings(request):
    user_profile_id = request.session['profile_data']['profile_data']['profile_id']
    bookings = ServiceBooking.objects.filter(user_id=user_profile_id)
    return render(request, 'ovros_dashboard/user_dashboard/user_dashboard_bookings_view.html'
                  , {
                    'section':'dashboard',
                    'bookings': bookings
                  })


@login_required()
def cancel_user_booking(request, booking_id):
    ServiceBooking.objects.filter(id=booking_id).delete()
    messages.warning(request, "Booking Cancelled Success...")
    return redirect('view_booking')
