from django.urls import path
from . import views

urlpatterns =[
    path('admin-overview', views.admin_overview, name='admin_overview'),
    path('admin-users', views.admin_users, name='admin_users'),
    path('admin-users/register', views.admin_register_user, name='admin_users_register'),
    path('admin-shops', views.admin_shops, name='admin_shops')
]