from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ovros_user_module.forms import UserRegistrationForm, UserEditForm, UserProfileEditForm
from ovros_user_module.models import UserProfile, ShopProfile
from ovros_service_module.models import Service
from ovros_booking.views import ServiceBooking
from ovros_booking.forms import BookingStatusChangeForm
from django.contrib.auth.models import User

from ovros_booking.models import ServiceBooking


@login_required
def admin_overview(request):
    no_of_services = Service.objects.count()
    return render(request, 'ovros_dashboard/admin_dashboard/admin_dashboard_overview.html',
                  {'section': 'dashboard', 'no_of_services': no_of_services})


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
    no_of_services = Service.objects.count()
    return render(request,
                  'ovros_dashboard/shop_dashboard/shop_dashboard_overview.html',
                  {'section': 'dashboard', 'no_of_services': no_of_services})


@login_required()
def shop_services(request):
    current_user = request.user
    user_id = current_user.id
    shop = ShopProfile.objects.get(user_id=user_id)
    shop_id = shop.id
    no_of_services = Service.objects.filter(shop_id=shop_id).count()
    return render(request, 'ovros_dashboard/shop_dashboard/shop_dashboard_services.html',
                  {'section': 'dashboard', 'no_of_services': no_of_services })


@login_required()
def shop_bookings(request):
    return render(request, 'ovros_dashboard/shop_dashboard/shop_dashboard_bookings.html', {'section': 'dashboard'})


@login_required()
def shop_bookings_view(request):

    if request.method == 'POST':
        print("Booking Data Received...")
        print("Booking id : ", request.POST['booking_id'])
        print("Booking STATUS : ", request.POST['booking_status'])
        booking_id = request.POST['booking_id']
        booking_status = request.POST['booking_status']
        booking_rec = ServiceBooking.objects.get(id=booking_id)
        booking_rec.booking_status = booking_status
        booking_rec.save()

    shop_profile_id = request.session['profile_data']['profile_data']['profile_id']
    shop_booking_list = ServiceBooking.objects.filter(service__shop_id=shop_profile_id)
    book_status_chng_form = BookingStatusChangeForm()
    return render(request,
                  'ovros_dashboard/shop_dashboard/shop_dashboard_bookings_view.html',
                  {'pro_id': shop_profile_id,
                   'section':'dashboard',
                   'shop_bookings': shop_booking_list,
                   'action_form': book_status_chng_form})


@login_required()
def shop_services_list(request):
    print(request.POST['profile_id'])
    pro_id = request.POST['profile_id']
    services = Service.objects.filter(shop_id=pro_id)
    return render(request,
                  'ovros_dashboard/shop_dashboard/shop_dashboard_service_list.html',
                  {'service': 'dashboard', 'services': services})


def shop_payments(request, profile_id):
    print(profile_id)
    return render(request, 'ovros_dashboard/shop_dashboard/shop_dashboard_payment.html', {'section': 'dashboard'})


def shop_reports(request):
    return render(request, 'ovros_dashboard/shop_dashboard/shop_dashboard_report.html', {'section': 'dashboard'})


@login_required()
def user_overview(request):
    user_id = request.session['profile_data']['profile_data']['user_id']
    booking_count = ServiceBooking.objects.filter(user_id=user_id).count()
    return render(request, 'ovros_dashboard/user_dashboard/user_dashboard_overview.html',
                  {'section': 'dashboard',
                   'booking_count': booking_count
                   })


@login_required()
def user_booking(request):
    user_id = request.session['profile_data']['profile_data']['user_id']
    bookings = ServiceBooking.objects.filter(user_id=user_id)
    pending_bookings = bookings.filter(booking_status="PENDING").count()
    approved_bookings = bookings.filter(booking_status="APPROVED").count()
    canceled_bookings = bookings.filter(booking_status="CANCELED").count()
    return render(request,
                  'ovros_dashboard/user_dashboard/user_dashboard_bookings.html',
                  {'section': 'dashboard',
                   'bookings': bookings,
                   'pending_count': pending_bookings,
                   'approved_count': approved_bookings,
                   'canceled_count': canceled_bookings,
                   })


def user_payment(request):
    return render(request, 'ovros_dashboard/user_dashboard/user_dashboard_payment.html', {'section': 'dashboard'})


def user_favorites(request):
    return render(request, 'ovros_dashboard/user_dashboard/user_dashboard_favorites.html', {'section': 'dashboard'})


def user_profile(request):
    print('profile data in profile view :', request.session['profile_data']['profile_data'])
    user_id = request.session['profile_data']['profile_data']['user_id']
    profile_id = request.session['profile_data']['profile_data']['profile_id']
    profile = UserProfile.objects.get(id=profile_id)
    user_p_data = User.objects.get(id=user_id)
    print(user_p_data.first_name)
    return render(request,
                  'ovros_dashboard/user_dashboard/user_dashboard_profile.html',
                  {'section': 'dashboard',
                   'profile_d': user_p_data,
                   'profile': profile})


def user_profile_edit(request):
    user_id = request.session['profile_data']['profile_data']['user_id']
    profile_id = request.session['profile_data']['profile_data']['profile_id']
    user = User.objects.get(id=user_id)
    profile = UserProfile.objects.get(id=profile_id)
    if request.method == 'POST':
        user_edit_form = UserEditForm(request.POST)
        profile_edit_form = UserProfileEditForm(request.POST)
        if user_edit_form.is_valid() and profile_edit_form.is_valid():
            f_name = request.POST['first_name']
            l_name = request.POST['last_name']
            email = request.POST['email']
            contact_number = request.POST['contact_number']
            user.first_name = f_name
            user.last_name = l_name
            user.email = email
            profile.contact_number = contact_number
            try:
                profile.photo = request.FILES['photo']
            except:
                pass
            user.save()
            profile.save()
            return user_profile(request)
    else:
        print(user.username)
        initial_user_dict = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }

        initial_user_profile_dict = {
            'contact_number': profile.contact_number,
            'photo': profile.photo
        }
        u_form = UserEditForm(initial=initial_user_dict)
        p_form = UserProfileEditForm(initial=initial_user_profile_dict)
        return render(request,
                      'ovros_dashboard/user_dashboard/user_dashboard_profile_edit.html',
                      {'section': 'dashboard', 'u_form': u_form, 'p_form': p_form})