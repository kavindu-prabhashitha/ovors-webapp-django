from django.urls import path
from . import views

urlpatterns =[

    # admin dashboard urls
    path('admin-overview', views.admin_overview, name='admin_overview'),
    path('admin-users', views.admin_users, name='admin_users'),
    path('admin-users/register', views.admin_register_user, name='admin_users_register'),
    path('admin-shops', views.admin_shops, name='admin_shops'),

    # shop dashboard urls
    path('shop-overview', views.shop_overview, name='shop_overview'),
    path('shop-services', views.shop_services, name='shop_services'),
    path('shop-bookings', views.shop_bookings, name='shop_bookings'),
    path('shop-payments', views.shop_payments, name='shop_payments'),
    path('shop-reports', views.shop_reports, name='shop_reports'),

    # shop dashboard urls
    path('user-overview', views.user_overview, name='user_overview'),
    path('user-bookings', views.user_booking, name='user_bookings'),
    path('user-payments', views.user_payment, name='user_payments'),
    path('user-reports', views.user_payment, name='user_reports'),
    path('user-favorites', views.user_favorites, name='user_favorite'),

]