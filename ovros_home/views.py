from django.shortcuts import render
from ovros_service_module.models import Service
from .forms import ServiceSearchForm


def home(request):
    search_form = ServiceSearchForm()
    return render(request, 'home/index.html', {'form': search_form})


def services(request):
    all_services = Service.objects.all()
    return render(request, 'services/service_list.html', {'services': all_services})


def search(request):
    found_results = []
    if request.method == 'GET':
        search_keyword = request.GET.get('search_by_Keyword')
        key = search_keyword.split()
        size_of_key = len(key)
        print("Array Size : ", size_of_key)
        try:
            for e in key:
                results = Service.objects.filter(service_name__icontains=e)
                found_results += results
            if size_of_key == 0:
                found_results = Service.objects.all()
                return render(request, 'services/service_list.html', {'services': found_results})
            return render(request, 'services/service_list.html', {'services': found_results})
        except Service.DoesNotExist:
            found_results = Service.objects.all()
            print(found_results)
            return render(request, 'services/service_list.html', {'services': found_results})

    else:
        return render(request, 'home/index.html')
