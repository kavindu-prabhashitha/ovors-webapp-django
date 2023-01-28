import datetime

from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from ovros_user_module.forms import UserRegistrationForm, UserEditForm, UserProfileEditForm
from ovros_user_module.models import UserProfile, ShopProfile
from ovros_service_module.models import Service
from django.contrib import messages

from ovros_booking.forms import BookingStatusChangeForm, ServiceStatusChangeForm, ServicePaymentStatusChangeForm
from ovros_service_module.forms import ServiceEditForm
from django.contrib.auth.models import User

from ovros_payment_module.forms import ShopBankDetAddForm, ShopBankDetEditForm
from ovros_payment_module.models import ShopPaymentDetail

from ovros_booking.models import ServiceBooking
from .helpers import save_pdf


@login_required
def admin_overview(request):
    no_of_services = Service.objects.count()
    no_of_shops = ShopProfile.objects.count()
    no_of_users = UserProfile.objects.count()
    return render(request, 'ovros_dashboard/admin_dashboard/admin_dashboard_overview.html',
                  {'section': 'dashboard',
                   'no_of_services': no_of_services,
                   'no_of_shops': no_of_shops,
                   'no_of_users': no_of_users,
                   })


@login_required
def admin_users(request):
    no_of_users = UserProfile.objects.count()
    return render(request, 'ovros_dashboard/admin_dashboard/admin_dashboard_users.html',
                  {'section': 'dashboard',
                   'no_of_users': no_of_users})


def admin_users_view(request):
    return render(request, 'ovros_dashboard/admin_dashboard/admin_dashboard_users_view.html',
                  {'section': 'dashboard'}
                  )

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
                          'ovros_dashboard/admin_dashboard/admin_dashboard_overview.html',
                          {'section': 'dashboard'})
    else:
        user_form = UserRegistrationForm()
        return render(request,
                      'ovros_dashboard/admin_dashboard/admin_dashboard_users_register.html',
                      {'user_form': user_form,
                       'section': 'dashboard'}
                      )


def shop_overview(request):
    shop_profile_id = request.session['profile_data']['profile_data']['profile_id']
    shop_booking_count = ServiceBooking.objects.filter(service__shop_id=shop_profile_id).count()
    no_of_services = Service.objects.count()
    return render(request,
                  'ovros_dashboard/shop_dashboard/shop_dashboard_overview.html',
                  {'section': 'dashboard',
                   'no_of_services': no_of_services,
                   'no_of_bookings': shop_booking_count
                   })


@login_required()
def shop_services(request):
    current_user = request.user
    user_id = current_user.id
    shop = ShopProfile.objects.get(user_id=user_id)
    shop_id = shop.id
    no_of_services = Service.objects.filter(shop_id=shop_id).count()
    return render(request,
                  'ovros_dashboard/shop_dashboard/shop_dashboard_services.html',
                  {'section': 'dashboard',
                   'no_of_services': no_of_services })


def shop_service_ongoing(request):
    current_user = request.user
    user_id = current_user.id

    if request.method == 'POST':
        print("Booking id : ", request.POST['booking_id'])
        print("Service STATUS : ", request.POST['service_status'])
        booking_id = request.POST['booking_id']
        booking_service_status = request.POST['service_status']
        booking_rec = ServiceBooking.objects.get(id=booking_id)
        booking_rec.service_status = booking_service_status
        booking_rec.save()

    shop = ShopProfile.objects.get(user_id=user_id)
    shop_service_bookings = ServiceBooking.objects.filter(service__shop_id=shop.id)
    service_status_chng_form = ServiceStatusChangeForm()
    return render(request,
                  'ovros_dashboard/shop_dashboard/shop_dashboard_service_ongoing.html',
                  {
                      'section': 'dashboard',
                      'shop_services': shop_service_bookings,
                      'action_form': service_status_chng_form
                  })


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
                   'section': 'dashboard',
                   'shop_bookings': shop_booking_list,
                   'action_form': book_status_chng_form})


@login_required()
def shop_services_list(request):
    pro_id = request.session['profile_data']['profile_data']['profile_id']
    services = Service.objects.filter(shop_id=pro_id)
    return render(request,
                  'ovros_dashboard/shop_dashboard/shop_dashboard_service_list.html',
                  {'section': 'dashboard', 'services': services})


def shop_service_edit(request, service_id):
    shop_profile_id = request.session['profile_data']['profile_data']['profile_id']
    shop_profile_role = request.session['profile_data']['profile_data']['profile_role']
    service_rec = Service.objects.get(id=service_id)
    old_img = service_rec.service_image

    is_verified = check_service_edit_permission(service_rec ,request.user.id, shop_profile_role)
    print('is user verified :', is_verified)
    if request.method == 'POST':
        service_form = ServiceEditForm(request.POST, request.FILES or None)
        if service_form.is_valid():
            cd = service_form.cleaned_data
            service_rec.service_name = cd['service_name']
            if 'service_image' in request.FILES:
                service_rec.service_image = cd['service_image']
            else:
                service_rec.service_image = old_img
            service_rec.service_description = cd['service_description']
            service_rec.service_duration = cd['service_duration']
            service_rec.service_price = cd['service_price']
            service_rec.is_for_bike = cd['is_for_bike']
            service_rec.is_for_van = cd['is_for_van']
            service_rec.is_for_car = cd['is_for_car']
            service_rec.is_for_suv = cd['is_for_suv']
            service_rec.is_for_lorry = cd['is_for_lorry']

            service_rec.save()
            messages.success(request, "Service Updated ...")
            return redirect('shop_services_list')
    else:
        initial_rec_dic = {
                'service_name': service_rec.service_name,
                'service_image': service_rec.service_image,
                'service_description': service_rec.service_description,
                'service_duration': service_rec.service_duration,
                'service_price': service_rec.service_price,
                'is_for_bike': service_rec.is_for_bike,
                'is_for_van': service_rec.is_for_van,
                'is_for_car': service_rec.is_for_car,
                'is_for_suv': service_rec.is_for_suv,
                'is_for_lorry': service_rec.is_for_lorry,
        }

        service_edit_form = ServiceEditForm(initial=initial_rec_dic)
        return render(request, 'ovros_dashboard/shop_dashboard/shop_dashboard_service_edit.html',
                      {
                        'section': 'dashboard',
                        'service_edit_form': service_edit_form}
                      )


def check_service_edit_permission(service, user_id, user_role):
    if service.shop.user.id == user_id:
        return True
    else:
        return False


def shop_payments(request):
    return render(request, 'ovros_dashboard/shop_dashboard/shop_dashboard_payment.html', {'section': 'dashboard'})


def shop_payments_view(request):
    user_id = request.user.id
    shop = ShopProfile.objects.get(user_id=user_id)
    shop_service_bookings = ServiceBooking.objects.filter(service__shop_id=shop.id)
    service_status_chng_form = ServicePaymentStatusChangeForm()
    return render(request, 'ovros_dashboard/shop_dashboard/shop_dashboard_payment_view.html',
                  {
                      'section': 'dashboard',
                      'shop_services': shop_service_bookings,
                      'action_form': service_status_chng_form
                  })


def shop_reports(request):
    return render(request, 'ovros_dashboard/shop_dashboard/shop_dashboard_report.html', {'section': 'dashboard'})


def shop_profile(request):
    user_id = request.session['profile_data']['profile_data']['user_id']
    shop_profile_id = request.session['profile_data']['profile_data']['profile_id']

    if request.method == 'POST':
        if request.POST['edit_payment'] == '0':
            payment_form = ShopBankDetAddForm(request.POST)
            if payment_form.is_valid():
                p_detail = ShopPaymentDetail()
                p_detail.shop_profile = ShopProfile.objects.get(id=shop_profile_id)
                p_detail.bank_name = request.POST['bank_name']
                p_detail.bank_branch = request.POST['bank_branch']
                p_detail.account_no = request.POST['account_no']
                p_detail.account_name = request.POST['account_name']
                p_detail.save()
        if request.POST['edit_payment'] == '1':
            payment_edit_form = ShopBankDetEditForm(request.POST)
            if payment_edit_form.is_valid():
                shop_pro = ShopProfile.objects.get(id=shop_profile_id)
                p_detail = ShopPaymentDetail.objects.get(shop_profile=shop_pro)
                p_detail.bank_name = request.POST['bank_name']
                p_detail.bank_branch = request.POST['bank_branch']
                p_detail.account_no = request.POST['account_no']
                p_detail.account_name = request.POST['account_name']
                p_detail.save()

    profile = ShopProfile.objects.get(id=shop_profile_id)
    shop_p_data = User.objects.get(id=user_id)
    try:
        payment_detail = ShopPaymentDetail.objects.get(shop_profile_id=profile.id)
        bank_det_available = True
        intial_dict = {
            'bank_name': payment_detail.bank_name,
            'bank_branch': payment_detail.bank_branch,
            'account_no': payment_detail.account_no,
            'account_name': payment_detail.account_name
        }
    except ShopPaymentDetail.DoesNotExist:
        payment_detail = ShopPaymentDetail()
        intial_dict = {}
        bank_det_available = False

    payment_form = ShopBankDetAddForm(initial=intial_dict)
    print(shop_p_data.email)
    return render(request,
                  'ovros_dashboard/shop_dashboard/shop_dashboard_profile.html',
                  {'section': 'dashboard',
                   'bank_detail_availability': bank_det_available,
                   'payment_detail': payment_detail,
                   'payment_add_form': payment_form,
                   'profile_d': shop_p_data,
                   'profile': profile})


def shop_profile_edit(request):
    user_id = request.session['profile_data']['profile_data']['user_id']
    profile_id = request.session['profile_data']['profile_data']['profile_id']
    user = User.objects.get(id=user_id)
    profile = ShopProfile.objects.get(id=profile_id)


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


def generate_booking_detail(request, booking_id):
    booking = ServiceBooking.objects.get(id=booking_id)

    params = {
        'today': datetime.date.today(),
        'booking': booking
    }
    file_res = save_pdf(params)
    return file_res
