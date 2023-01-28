from django.urls import path
from . import views

urlpatterns = [
    path('booking-add/<service_id>', views.add_booking, name='add_booking'),
    path('booking-view/', views.view_user_bookings, name='view_booking'),
    path('booking-cancel/<booking_id>', views.cancel_user_booking, name='cancel_booking'),
]