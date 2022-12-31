from django.urls import path
from django.contrib.auth import views as auth_view
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', auth_view.LoginView.as_view(), name='login'),
    path('logout/', auth_view.LogoutView.as_view(), name='logout'),
    # post views
    # path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('register/user', views.user_register, name='user_register'),
    path('register/shop', views.shop_register, name='shop_register'),
    path('edit/', views.edit, name='edit'),

    path('password_change/', auth_view.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done', auth_view.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # reset password url
    path('password_reset', auth_view.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done', auth_view.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done', auth_view.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

