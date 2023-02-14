from django.urls import path
from . import views

urlpatterns = [
    path('shop-report-generate', views.generate_report_shop, name='shop_generate_report'),
    path('user-report-generate', views.generate_report_user, name='user_generate_report'),

]