from django.shortcuts import render
from ovros_service_module.models import Service
from ovros_user_module.models import ShopProfile
from .forms import ServiceSearchForm, ServiceSearchForm01, ServiceSearchForm02, ServiceSearchByShop
from django.contrib import messages


def home(request):
    """
    Landing page of the ovros (Online Vehicle Repairing Ordering System)
    :param request:
    :return:
    """
    search_form = ServiceSearchForm()
    return render(request, 'home/index.html', {'form': search_form})


def services(request):
    """
    list all available services in the system
    :param request:
    :return:
    """
    if request.method == 'GET':
        search(request)

        search_form01 = ServiceSearchForm01()
        search_form02 = ServiceSearchForm02()
        all_services = Service.objects.all()
        return render(request, 'services/service_list.html', {
            'services': all_services,
            'form01': search_form01,
            'form02': search_form02,
        })


def service_detail(request, service_id):
    """
    Return service details for selected service
    :param request:
    :param service_id:
    :return:
    """
    if request.user.is_authenticated:
        user_profile_role = request.session['profile_data']['profile_data']['profile_role']
        print(service_id, '  ', user_profile_role)
    else:
        user_profile_role = "USER_CUSTOMER"
    service = Service.objects.get(id=service_id)

    return render(request, 'services/service_detail.html',
                  {'service': service,
                   'user_role': user_profile_role
                   })
    #return render(request, 'services/service_detail.html', {'service': service})


def search(request):
    """
    Search available services by available filters
    :param request:
    :return:
    """
    all_services = Service.objects.all()
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
                try:
                    for e in key:
                        all_services = all_services.filter(service_name__icontains=e)
                except Service.DoesNotExist:
                    print("Record Not Found")
        if "search_by_district" in request.GET:
            if request.GET.get("search_by_district") == "SelectDistrict":
                print("Search by district is empty")
            else:
                print("Search Contains district")
                all_services = all_services.filter(shop__shop_address_district=search_district)
                print(all_services)

        if "search_by_city" in request.GET:
            if request.GET.get("search_by_city") == "SelectCity":
                print("Search_by_city is empty")
            else:
                print("Search Contains city")
                all_services = all_services.filter(shop__shop_address_city=search_city)
        if "search_by_vehicle" in request.GET:
            if request.GET.get("search_by_vehicle") == "NON":
                print("search_by_vehicle is empty")
            else:
                print("Search Contains vehicle")
                if request.GET.get("search_by_vehicle") == "CAR":
                    all_services = all_services.filter(is_for_car=1)
                elif request.GET.get("search_by_vehicle") == "VAN":
                    all_services = all_services.filter(is_for_van=1)
                elif request.GET.get("search_by_vehicle") == "BIKE":
                    all_services = all_services.filter(is_for_bike=1)
                elif request.GET.get("search_by_vehicle") == "SUV":
                    all_services = all_services.filter(is_for_suv=1)

        print("found results : ", all_services.count())
        search_form01 = ServiceSearchForm01()
        search_form02 = ServiceSearchForm02()
        return render(request, 'services/service_list.html', {
            'services': all_services,
            'form01': search_form01,
            'form02': search_form02,
        })

    else:
        return render(request, 'home/index.html')


def shops(request):
    all_shops = ShopProfile.objects.all()
    if request.method == "POST":
        form = ServiceSearchByShop(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            key_word = cd['search_by_shop']
            print(key_word)
            print("Shop Search value = ", cd['search_by_shop'])
            if len(key_word) == 0:
                all_shops = ShopProfile.objects.all()
            else:
                all_shops = all_shops.filter(shop_name__icontains=key_word)
                if all_shops.count() == 0:
                    messages.warning(request, f"No Shops found contains the name '{key_word}'")
                    all_shops = ShopProfile.objects.all()
            return render(request, "shops/shop_list.html", {"shops_profiles": all_shops, 'form': form})

    else:
        form = ServiceSearchByShop()
        return render(request, "shops/shop_list.html", {
            "shops_profiles": all_shops,
            'form': form
        })


def shop_detail(request, shop_id):
    shop_d = ShopProfile.objects.get(id=shop_id)
    shop_services = Service.objects.filter(shop=shop_id)
    return render(request, "shops/shop_detail.html", {
        "profile": shop_d,
        "shop_services": shop_services
    })
