from django.shortcuts import render
from ovros_service_module.models import Service


def home(request):
    return render(request, 'home/index.html')


def services(request):
    all_services = Service.objects.all()
    return render(request, 'services/service_list.html', {'services': all_services})
