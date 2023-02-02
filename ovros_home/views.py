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
    all_services = Service.objects.all()
    found_results = []
    if request.method == 'GET':
        search_keyword = request.GET.get('search_by_Keyword')
        search_district = request.GET.get('search_by_district')
        search_city = request.GET.get('search_by_city')
        search_vehicle = request.GET.get('search_by_vehicle')
        print("Array Size : ", search_keyword, search_district, search_city, search_vehicle)
        if "search_by_Keyword" in request.GET:
            if request.GET.get("search_by_Keyword") == "":
                print("Search keyword is empty")
            else:
                print("Search Contains keyword")
                key = search_keyword.split()
                size_of_key = len(key)
                try:
                    for e in key:
                        result = all_services.filter(service_name__icontains=e)
                        found_results.append(result)
                    print(type(found_results))
                    print(found_results)
                except Service.DoesNotExist:
                    found_results = Service.objects.all()
                    print(found_results)
        if "search_by_district" in request.GET:
            if request.GET.get("search_by_district") == "":
                print("Search by district is empty")
            else:
                print("Search Contains district")
                # found_results = found_results.filter(shop__shop_address_district__contains=search_district)

        if "search_by_city" in request.GET:
            if request.GET.get("search_by_district") == "":
                print("Search_by_city is empty")
            else:
                print("Search Contains city")
                # found_results = found_results.filter(shop__shop_address_city=search_city)
        if "search_by_vehicle" in request.GET:
            if request.GET.get("search_by_vehicle") == "NON":
                print("search_by_vehicle is empty")
            else:
                print("Search Contains vehicle")
        print("found results : ", )
        return render(request, 'services/service_list.html', {'services': found_results[0]})

    else:
        return render(request, 'home/index.html')
