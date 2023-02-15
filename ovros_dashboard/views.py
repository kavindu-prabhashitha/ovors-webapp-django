import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ovros_user_module.forms import UserRegistrationForm, UserEditForm, UserProfileEditForm, ShopProfileCreationForm
from ovros_user_module.models import UserProfile, ShopProfile
from ovros_service_module.models import Service
from django.contrib import messages
from ovros_booking.forms import (
    BookingStatusChangeForm,
    ServiceStatusChangeForm,
    ServicePaymentStatusChangeForm,
    ServiceBookingTimeAdd
)
from ovros_service_module.forms import ServiceEditForm
from django.contrib.auth.models import User
from ovros_payment_module.forms import ShopBankDetAddForm, ShopBankDetEditForm
from ovros_payment_module.models import ShopPaymentDetail
from ovros_booking.models import ServiceBooking
from .helpers import save_pdf
from common.enums import (
    BOOKING_STATUS,
    PAYMENT_STATUS,
    PAYMENT_DEFAULT_SLIP
)
from ovros_payment_module.forms import PaymentProceedForm
from ovros_payment_module.models import ShopPaymentProceed


def shop_overview(request):
    shop_profile_id = request.session['profile_data']['profile_data']['profile_id']
    shop_booking_count = ServiceBooking.objects.filter(service__shop_id=shop_profile_id).count()
    shop_payments_count = ShopPaymentProceed.objects.filter(payment_booking_id__service__shop_id=shop_profile_id).count()
    no_of_services = Service.objects.count()
    return render(request,
                  'ovros_dashboard/shop_dashboard/shop_dashboard_overview.html',
                  {'section': 'dashboard',
                   'no_of_services': no_of_services,
                   'no_of_bookings': shop_booking_count,
                   'no_of_payments': shop_payments_count
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
        print("Booking Time : ",  len(request.POST['booking_time']))
        booking_rec = ServiceBooking()
        if "booking_id" in request.POST:
            booking_id = request.POST['booking_id']
            booking_rec = ServiceBooking.objects.get(id=booking_id)
        else:
            print("Booking id not found")

        if "booking_status" in request.POST:
            booking_status = request.POST['booking_status']
            booking_rec.booking_status = booking_status
        else:
            print("Booking Status not found")

        if "booking_time" in request.POST:
            if len(request.POST['booking_time']) == 0:
                print("Booking Time Not Assigned")
            else:
                booking_time = request.POST['booking_time']
                booking_rec.booking_time = booking_time
        else:
            print("Booking Time not found")

        booking_rec.save()

    shop_profile_id = request.session['profile_data']['profile_data']['profile_id']
    shop_booking_list = ServiceBooking.objects.filter(service__shop_id=shop_profile_id)
    book_status_chng_form = BookingStatusChangeForm()
    book_time_chng_form = ServiceBookingTimeAdd()
    return render(request,
                  'ovros_dashboard/shop_dashboard/shop_dashboard_bookings_view.html',
                  {'pro_id': shop_profile_id,
                   'section': 'dashboard',
                   'shop_bookings': shop_booking_list,
                   'action_form': book_status_chng_form,
                   'action_form_booking_time': book_time_chng_form,
                   })


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
    shop_profile_id = request.session['profile_data']['profile_data']['profile_id']
    user_id = request.user.id
    shop = ShopProfile.objects.get(user_id=user_id)
    shop_service_bookings = ServiceBooking.objects.filter(service__shop_id=shop.id)
    shop_payments_count = ShopPaymentProceed.objects.filter(payment_booking_id__service__shop_id=shop_profile_id).count()
    shop_payments_count_pending = shop_service_bookings.filter(payment_status="PAYMENT_PENDING").count()
    return render(request, 'ovros_dashboard/shop_dashboard/shop_dashboard_payment.html', {
        'section': 'dashboard',
        'shop_pay_count': shop_payments_count,
        'shop_pay_pending_count': shop_payments_count_pending

    })


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


def shop_payments_verify(request):
    # booking_id = 0
    if request.method == 'POST' and ('booking_id_pv' in request.POST):
        p_status_chg_form = ServicePaymentStatusChangeForm()
        print("Incoming post request from payment view")
        booking_id = request.POST['booking_id_pv']
        b_data = ServiceBooking.objects.get(id=booking_id)
        print("Booing id at payment verify : ", booking_id)
        try:
            b_pay_proceed = ShopPaymentProceed.objects.get(payment_booking_id_id=booking_id)
        except ShopPaymentProceed.DoesNotExist:
            b_pay_proceed = ShopPaymentProceed()
            b_pay_proceed.payment_slip = PAYMENT_DEFAULT_SLIP

        return render(request, 'ovros_dashboard/shop_dashboard/shop_dashboard_payment_verify.html',
                      {'section': 'dashboard',
                       'booking_data': b_data,
                       'payment_verify_data': b_pay_proceed,
                       'p_status_chg_form': p_status_chg_form
                       })

    if request.method == 'POST' and ('proceed_payment_pv_verify' in request.POST):
        payment_status_chng_form = ServicePaymentStatusChangeForm(request.POST)
        if payment_status_chng_form.is_valid():
            booking_id = request.POST['booking_id']
            b_data = ServiceBooking.objects.get(id=booking_id)
            b_data.payment_status = request.POST['payment_status']
            print("Incoming post request from payment verify : ", b_data.payment_status)
            b_data.save()
            messages.success(request, "Payment Status updated")
            return redirect('shop_payments_view')
        print("Incoming post request from payment verify")
    return render(request, 'ovros_dashboard/shop_dashboard/shop_dashboard_payment_verify.html')


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

    if request.method == 'POST':
        s_form = ShopProfileCreationForm(request.POST)
        if s_form.is_valid():
            c_data = s_form.cleaned_data
            print(c_data)
            profile.shop_name = c_data['shop_name']
            profile.shop_address_no = c_data['shop_address_no']
            profile.shop_address_city = c_data['shop_address_city']
            profile.shop_address_district = c_data['shop_address_district']
            profile.shop_contact = c_data['shop_contact']
            profile.save()
            messages.success(request, "Shop Profile Updated..")
            return redirect('shop_profile')
        else:
            return render(request, "ovros_dashboard/shop_dashboard/shop_dashboard_profile_edit.html", {
                'section': 'dashboard',
                's_form': s_form
            })

    else:
        intial_dict = {
            'shop_name': profile.shop_name,
            'shop_address_no': profile.shop_address_no,
            "shop_address_street": profile.shop_address_street,
            'shop_address_city': profile.shop_address_city,
            'shop_address_district': profile.shop_address_district,
            'shop_contact': profile.shop_contact

        }
        s_form = ShopProfileCreationForm(initial=intial_dict)
        return render(request, "ovros_dashboard/shop_dashboard/shop_dashboard_profile_edit.html",{
            'section': 'dashboard',
            's_form': s_form
        })


@login_required()
def user_overview(request):
    user_id = request.session['profile_data']['profile_data']['user_id']
    profile_id =  request.session['profile_data']['profile_data']['profile_id']
    booking_count = ServiceBooking.objects.filter(user_id=user_id).count()
    payment_count = ShopPaymentProceed.objects.filter(payment_user_pro_id_id=profile_id).count()
    return render(request, 'ovros_dashboard/user_dashboard/user_dashboard_overview.html',
                  {'section': 'dashboard',
                   'booking_count': booking_count,
                   'payment_count': payment_count,
                   })


@login_required()
def user_booking(request):
    user_profile_id = request.session['profile_data']['profile_data']['profile_id']
    bookings = ServiceBooking.objects.filter(user_id=user_profile_id)
    print("User Id : ", user_profile_id)
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


def user_payment_view(request):
    pro_id = request.session['profile_data']['profile_data']['profile_id']
    if request.method == 'POST' and ('proceed_payment' in request.POST):
        print("payment proceed form")
        p_form = PaymentProceedForm(request)
        profile_id = pro_id
        if p_form.is_valid():
            if request.POST['proceed_payment'] == '1':
                if "payment_slip" in request.FILES:
                    slip = request.FILES['payment_slip']
                    if 'payment_note' in request.POST:
                        note = request.POST['payment_note']
                    else:
                        note = "Null"
                    b_id = request.POST['booking_id']
                    user_pro = UserProfile.objects.get(id=profile_id)
                    b_data = ServiceBooking.objects.get(id=b_id)
                    spp = ShopPaymentProceed()
                    spp.payment_slip = slip
                    spp.payment_note = note
                    spp.payment_booking_id = b_data
                    spp.payment_user_pro_id = user_pro
                    b_data.payment_status = PAYMENT_STATUS[1][0]
                    b_data.save()
                    spp.save()
                    messages.success(request, "Payment details submitted successfully..")
                    return redirect('user_payments_view')

    if request.method == 'POST':
        booking_id = request.POST['booking_id']
        booking_data = ServiceBooking.objects.get(id=booking_id)
        print('Booking id from payment proceed : ', booking_id)
        payment_proceed_form = PaymentProceedForm()
        return render(request, 'ovros_dashboard/user_dashboard/user_dashboard_payment_proceed.html', {
            'section': 'dashboard',
            'booking_id': booking_id,
            'booking_data': booking_data,
            'form': payment_proceed_form
        })
    else:
        user_bookings = ServiceBooking.objects.filter(user_id=pro_id)

        return render(request, 'ovros_dashboard/user_dashboard/user_dashboard_payment_view.html', {
            'section': 'dashboard',
            "user_bookings": user_bookings
        })


def user_payment_proceed(request):
    booking_id = request.POST['booking_id']
    print('Booking id from payment proceed : ', booking_id)
    return render(request, 'ovros_dashboard/user_dashboard/user_dashboard_payment_proceed.html')


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

