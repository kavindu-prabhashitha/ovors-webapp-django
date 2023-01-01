from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ovros_user_module.forms import UserRegistrationForm
from ovros_user_module.models import UserProfile


@login_required
def admin_overview(request):
    return render(request, 'ovros_dashboard/admin_dashboard/admin_dashboard_overview.html', {'section': 'dashboard'})


@login_required
def admin_users(request):
    return render(request, 'ovros_dashboard/admin_dashboard/admin_dashboard_users.html', {'section': 'dashboard'})


@login_required
def admin_shops(request):
    return render(request, 'ovros_dashboard/admin_dashboard/admin_dashboard_shops.html', {'section': 'dashboard'})


@login_required
def admin_register_user(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.save()
            UserProfile.objects.create(user=new_user, user_role='USER_CUSTOMER')
            return render(request,
                          'ovros_dashboard/admin_dashboard/admin_dashboard_overview.html')
    else:
        user_form = UserRegistrationForm()
        return render(request,
                      'ovros_dashboard/admin_dashboard/admin_dashboard_users_register.html',
                      {'user_form': user_form}
                      )


def shop_overview(request):
    return render(request, 'ovros_dashboard/shop_dashboard/shop_dashboard_overview.html', {'section': 'dashboard'})


def shop_services(request):
    return render(request, 'ovros_dashboard/shop_dashboard/shop_dashboard_services.html', {'section': 'dashboard'})


def shop_bookings(request):
    return render(request, 'ovros_dashboard/shop_dashboard/shop_dashboard_bookings.html', {'section': 'dashboard'})


def shop_payments(request):
    return render(request, 'ovros_dashboard/shop_dashboard/shop_dashboard_payment.html', {'section': 'dashboard'})


def shop_reports(request):
    return render(request, 'ovros_dashboard/shop_dashboard/shop_dashboard_report.html', {'section': 'dashboard'})


def user_overview(request):
    return render(request, 'ovros_dashboard/user_dashboard/user_dashboard_overview.html', {'section': 'dashboard'})


def user_booking(request):
    return render(request, 'ovros_dashboard/user_dashboard/user_dashboard_bookings.html', {'section': 'dashboard'})


def user_payment(request):
    return render(request, 'ovros_dashboard/user_dashboard/user_dashboard_payment.html', {'section': 'dashboard'})


def user_favorites(request):
    return render(request, 'ovros_dashboard/user_dashboard/user_dashboard_favorites.html', {'section': 'dashboard'})
