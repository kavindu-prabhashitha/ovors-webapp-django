from django.urls import path
from . import views

urlpatterns = [
    path('service_add', views.service_add, name='service_add'),
    path('service_list', views.service_list, name='service_list'),
]