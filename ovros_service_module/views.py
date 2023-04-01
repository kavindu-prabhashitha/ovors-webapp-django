from django.shortcuts import render, redirect
from .forms import ServiceCreationForm
from ovros_user_module.views import ShopProfile
from .models import Service


def service_add(request):
    """
    Add Service by Service Shops
    :param request:
    :return:
    """
    user_profile_id = request.session['profile_data']['profile_data']['profile_id']
    user_profile_role = request.session['profile_data']['profile_data']['profile_role']
    if request.method == 'POST':
        form = ServiceCreationForm(request.POST, request.FILES or None)
        if form.is_valid():
            cd = form.cleaned_data
            role = request.POST.get('user_role', "")
            print(cd)
            print(role)
            print(request.user.id)
            try:
                if user_profile_role == 'USER_SHOP':
                    shop = ShopProfile.objects.get(user_id=request.user.id)
                    print(shop.shop_name)
                    new_service = Service()
                    new_service.shop = shop
                    new_service.service_name = cd['service_name']
                    new_service.service_price = cd['service_price']
                    new_service.service_duration = cd['service_duration']
                    new_service.service_description = cd['service_description']
                    new_service.is_for_car = cd['is_for_car']
                    new_service.is_for_suv = cd['is_for_suv']
                    new_service.is_for_van = cd['is_for_van']
                    new_service.is_for_lorry = cd['is_for_lorry']
                    new_service.is_for_bike = cd['is_for_bike']
                    new_service.is_for_long_vehicle = cd['is_for_long_vehicle']
                    if form.cleaned_data['service_image']:
                        new_service.service_image = form.cleaned_data['service_image']
                    new_service.save()
                    return redirect('shop_services_list')

            except ShopProfile.DoesNotExist:
                form = ServiceCreationForm()
                return render(request,
                              'ovros_dashboard/shop_dashboard/shop_dashboard_service_add.html',
                              {'section': 'dashboard', 'form': form})

            return render(request,
                          'ovros_dashboard/shop_dashboard/shop_dashboard_service_add.html',
                          {'section': 'dashboard', 'form': form}
                          )
    else:
        form = ServiceCreationForm()
        return render(request,
                      'ovros_dashboard/shop_dashboard/shop_dashboard_service_add.html',
                      {'section': 'dashboard', 'form': form})


def service_list(request):
    """
    Return All Available services
    :param request:
    :return:
    """
    return render(request,
                  'ovros_dashboard/shop_dashboard/shop_dashboard_service_list.html',
                  {'section': 'dashboard'})


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
