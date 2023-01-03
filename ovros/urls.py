from django.contrib import admin
from django.urls import path, include
from ovros_home.views import home, services
from ovros_user_module import urls as account_urls
from ovros_dashboard import urls as dashboard_urls
from ovros_service_module import urls as service_urls
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('services/', services, name='services'),
    path('admin/', admin.site.urls),
    path('account/', include(account_urls)),
    path('dashboard/', include(dashboard_urls)),
    path('service/', include(service_urls)),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
