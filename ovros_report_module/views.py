from django.shortcuts import render
from .forms import ShopReportGenerateForm, UserReportGenerateForm
from ovros_booking.models import ServiceBooking
import datetime
from ovros_dashboard.helpers import generate_pdf
from common.enums import USER_REPORT_TYPES


def generate_report_shop(request):
    """
    Generate Shop reports
    :param request:
    :return:
    """
    profile_id = request.session['profile_data']['profile_data']['profile_id']
    user_id = request.session['profile_data']['profile_data']['user_id']
    if request.method == 'POST':
        report_gen_form = ShopReportGenerateForm(request.POST)
        if report_gen_form.is_valid():
            cd = report_gen_form.cleaned_data
            print("Report Form Cleaned Data (Shop): ", cd)
            if cd['report_type'] == "ALL_SERVICES":
                return generate_booking_detail(request, user_id, profile_id, "User Booked Services", 1, 0)
            if cd['report_type'] == "ALL_PAYMENTS":
                return generate_booking_detail(request, user_id, profile_id, "User Confirmed Services", 0, 1)
        else:
            report_gen_form = ShopReportGenerateForm(request.POST)
            return render(request, 'ovros_dashboard/shop_dashboard/shop_dashboard_report_generate.html', {
                'section': 'dashboard',
                'form': report_gen_form
            })

    report_gen_form = ShopReportGenerateForm()
    return render(request, 'ovros_dashboard/shop_dashboard/shop_dashboard_report_generate.html', {
        'section': 'dashboard',
        'form': report_gen_form
    })


def generate_report_user(request):
    """
    Generate User Reports for specified requirements
    :param request:
    :return:
    """
    profile_id = request.session['profile_data']['profile_data']['profile_id']
    user_id = request.session['profile_data']['profile_data']['user_id']
    if request.method == 'POST':
        report_gen_form = UserReportGenerateForm(request.POST)
        if report_gen_form.is_valid():
            cd = report_gen_form.cleaned_data
            print("Report Form Cleaned Data (User) : ", cd)
            if cd['report_type'] == "BOOKED_SERVICES":
                return generate_booking_detail(request, user_id, profile_id, "User Booked Services", 1, 0)
            if cd['report_type'] == "CONFIRMED_SERVICES":
                return generate_booking_detail(request, user_id, profile_id, "User Confirmed Services", 0, 1)
        else:
            report_gen_form = UserReportGenerateForm(request.POST)
            return render(request, 'ovros_dashboard/user_dashboard/user_dashboard_report_generate.html', {
                'section': 'dashboard',
                'form': report_gen_form
            })
    report_gen_form = UserReportGenerateForm()
    return render(request, 'ovros_dashboard/user_dashboard/user_dashboard_report_generate.html', {
        'section': 'dashboard',
        'form': report_gen_form
    })


def generate_booking_detail(request, uid, pid, title, booked_service_r, confirmed_service_r):
    bookings = ServiceBooking.objects.filter(user_id=uid)

    if confirmed_service_r == 1:
        bookings = bookings.filter(booking_status="APPROVED")
    if booked_service_r == 1:
        pass

    params = {
        'title': title,
        'today': datetime.date.today(),
        'booked_services': bookings,
        'user_booked_services_report': booked_service_r,
        'user_confirmed_services_report': confirmed_service_r
    }
    file_res = generate_pdf(params, "booked_services.html", "user_booked_services_" + uid)
    return file_res
