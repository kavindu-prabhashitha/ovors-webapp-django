from django.shortcuts import render
from .forms import ServiceCreationForm
from ovros_user_module.views import ShopProfile
from .models import Service


def service_add(request):
    if request.method == 'POST':
        form = ServiceCreationForm(request.POST, request.FILES or None)
        if form.is_valid():
            cd = form.cleaned_data
            role = request.POST.get('user_role', "")
            print(cd)
            print(role)
            print(request.user.id)
            try:
                if role == '999':
                    shop = ShopProfile.objects.get(user_id=request.user.id)
                    print(shop.shop_name)
                    new_service = Service()
                    new_service.shop = shop
                    new_service.service_name = cd['service_name']
                    new_service.service_price = cd['service_price']
                    new_service.service_duration = cd['service_duration']
                    new_service.date_created = cd['date_created']
                    new_service.service_description = cd['service_description']
                    if form.cleaned_data['service_image']:
                        new_service.service_image = form.cleaned_data['service_image']
                    else:
                        default_file_path = 'images/service_img/card-header-default.jpg'
                        new_service.service_image = default_file_path

                    new_service.save()

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
    return render(request,
                  'ovros_dashboard/shop_dashboard/shop_dashboard_service_list.html',
                  {'section': 'dashboard'})


def service_detail(request, service_id):
    print(service_id)
    service = Service.objects.get(id=service_id)
    return render(request, 'services/service_detail.html', {'service': service})
