from django.urls import path
from . import views

urlpatterns =[
    # shop dashboard urls
    path('shop-overview', views.shop_overview, name='shop_overview'),
    path('shop-services', views.shop_services, name='shop_services'),
    path('shop-services-status', views.shop_service_ongoing, name='shop_services_ongoing'),
    path('shop-bookings', views.shop_bookings, name='shop_bookings'),
    path('shop-bookings-view', views.shop_bookings_view, name='shop_bookings_view'),

    path('shop-payments', views.shop_payments, name='shop_payments'),
    path('shop-payments-view', views.shop_payments_view, name='shop_payments_view'),
    path('shop-payments-verify', views.shop_payments_verify, name='shop_payments_verify'),
    path('shop-reports', views.shop_reports, name='shop_reports'),
    path('shop-profile', views.shop_profile, name='shop_profile'),
    path('shop-profile-edit', views.shop_profile_edit, name='shop_profile_edit'),
    path('shop-services-list', views.shop_services_list, name='shop_services_list'),
    path('shop-services-list/<service_id>', views.shop_service_delete, name='shop_services_delete'),
    path('shop-service-edit/<service_id>', views.shop_service_edit, name='shop_service_edit'),

    # shop dashboard urls
    path('user-overview', views.user_overview, name='user_overview'),
    path('user-bookings', views.user_booking, name='user_bookings'),
    path('user-payments', views.user_payment, name='user_payments'),
    path('user-payments-view', views.user_payment_view, name='user_payments_view'),
    path('user-payments-proceed', views.user_payment_proceed, name='user_payment_proceed'),
    path('user-reports', views.user_payment, name='user_reports'),
    path('user-favorites', views.user_favorites, name='user_favorite'),
    path('user-profile', views.user_profile, name='user_profile'),
    path('user-profile-edit', views.user_profile_edit, name='user_profile_edit'),
    path('user-print-booking/<booking_id>', views.generate_booking_detail, name='user_print_booking_pdf')

]