from django.shortcuts import render
from .forms import ServiceCreationForm
# Create your views here.


def service_add(request):
    form = ServiceCreationForm()
    return render(request,
                  'ovros_dashboard/shop_dashboard/shop_dashboard_service_add.html',
                  {'section': 'dashboard', 'form': form})


def service_list(request):
    return render(request,
                  'ovros_dashboard/shop_dashboard/shop_dashboard_service_list.html',
                  {'section': 'dashboard'})