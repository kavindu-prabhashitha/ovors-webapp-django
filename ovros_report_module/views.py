from django.shortcuts import render
from .forms import ShopReportGenerateForm, UserReportGenerateForm
# Create your views here.


def generate_report_shop(request):
    if request.method == 'POST':
        report_gen_form = ShopReportGenerateForm(request.POST)
        if report_gen_form.is_valid():
            cd = report_gen_form.cleaned_data
            print("Report Form Cleaned Data : ", cd)
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
    report_gen_form = UserReportGenerateForm()
    return render(request, 'ovros_dashboard/user_dashboard/user_dashboard_report_generate.html', {
        'section': 'dashboard',
        'form': report_gen_form
    })
