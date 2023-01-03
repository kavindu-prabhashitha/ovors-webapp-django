from django.shortcuts import render
from .forms import ServiceCreationForm
# Create your views here.


def service_add(request):
    if request.method == 'POST':
        form = ServiceCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'services/service_list.html')
    else:
        form = ServiceCreationForm()
        return render(request,
                      'ovros_dashboard/shop_dashboard/shop_dashboard_service_add.html',
                      {'section': 'dashboard', 'form': form})


def service_list(request):
    return render(request,
                  'ovros_dashboard/shop_dashboard/shop_dashboard_service_list.html',
                  {'section': 'dashboard'})


