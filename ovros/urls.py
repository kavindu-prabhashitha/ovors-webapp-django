from django.contrib import admin
from django.urls import path, include
from ovros_home.views import (home,
                              services,
                              service_detail,
                              shops,
                              shop_detail,
                              dashboard_new,
                              dashboard_new_user_booking,
                              dashboard_new_user_payments,
                              dashboard_new_user_reports,
                              dashboard_new_user_profile,
                              )
from ovros_user_module import urls as account_urls
from ovros_dashboard import urls as dashboard_urls
from ovros_home.views import search
from ovros_service_module import urls as service_urls
from ovros_report_module import urls as report_urls
from ovros_booking import urls as booking_urls
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = 'Ovros Admin'
admin.site.site_title = 'Ovros administration'
admin.site.index_title = 'Ovros Admin Dashboard'

urlpatterns = [
    # path('', home, name='home'),
    path('', home, name='home'),

    path('dashboard_new/', dashboard_new, name='dashboard_new'),
    path('dashboard_new/user/bookings', dashboard_new_user_booking, name='dashboard_new_user_bookings'),
    path('dashboard_new/user/payments', dashboard_new_user_payments, name='dashboard_new_user_payments'),
    path('dashboard_new/user/reports', dashboard_new_user_reports, name='dashboard_new_user_reports'),
    path('dashboard_new/user/profile', dashboard_new_user_profile, name='dashboard_new_user_profiles'),

    path('services/', services, name='services'),
    path('services/<int:service_id>', service_detail, name='service_detail_new'),
    path('shops/', shops, name='shops'),
    path('shops/<int:shop_id>', shop_detail, name='shop_detail'),
    path('search/', search, name='home_search'),
    path('admin/', admin.site.urls),
    path('account/', include(account_urls)),
    path('dashboard/', include(dashboard_urls)),
    path('service/', include(service_urls)),
    path('booking/', include(booking_urls)),
    path('report/', include(report_urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

