from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from ovros_service_module.models import Service
from .forms import (
    LoginForm,
    UserEditForm,
    UserRegistrationForm,
    UserProfileEditForm,
    ShopProfileCreationForm)

from .models import (
    UserProfile,
    ShopProfile)
from django.contrib import messages
from django.contrib.auth.models import User
from .profile_detail import ProfileData

# Create your views here.


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            print('session data : ', request.session.values())
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    redirect('dashboard')
                else:
                    return redirect('login')
            else:
                return HttpResponse("Invalid login")
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def dashboard(request):
    print('session data : ', request.session.keys())

    # user_profile_id = request.session['profile_data']['profile_data']
    # user_profile_id = request.session['profile_data']['profile_data']['profile_id']
    # print('user profile id at login : ', user_profile_id)
    try:
        user_profile = UserProfile.objects.get(user_id=request.user.id)
    except UserProfile.DoesNotExist:
        user_profile = ShopProfile.objects.get(user_id=request.user.id)

    profile_data = ProfileData(request)

    if user_profile.user_role == "USER_CUSTOMER":
        profile_data.add(request.user.id, user_profile.id, 'USER_CUSTOMER')
        print('user customer profile data : ', request.session['profile_data'])
        # return render(request,
        #               'ovros_dashboard/user_dashboard/user_dashboard_overview.html',
        #               {'section': 'dashboard',
        #                'user_role': '9',
        #                'profile_id': user_profile.id})
        return redirect('user_overview')

    if user_profile.user_role == "USER_ADMIN":
        profile_data.add(request.user.id, user_profile.id, 'USER_ADMIN')
        print('user admin profile data : ', request.session['profile_data'])
        # return render(request,
        #               'ovros_dashboard/admin_dashboard/admin_dashboard_overview.html',
        #               {'section': 'dashboard',
        #                'user_role': '99',
        #                'profile_id': user_profile.id})
        return redirect('admin:login')

    if user_profile.user_role == "USER_SHOP":
        profile_data.add(request.user.id, user_profile.id, 'USER_SHOP')
        print('user profile data : ', request.session['profile_data'])
        no_of_services = Service.objects.filter(shop_id=user_profile.id).count()
        # return render(request,
        #               'ovros_dashboard/shop_dashboard/shop_dashboard_overview.html',
        #               {'section': 'dashboard', 'no_of_services': no_of_services, 'user_role': '999',
        #                'profile_id': user_profile.id})
        return redirect('shop_overview')

    return login_required()


def register(request):
    return render(request, 'account/register.html')


def user_register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        user_profile_form = UserProfile(request.POST)
        if user_form.is_valid():
            # create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            # Save the User Object
            new_user.save()
            # create the user profile
            user_profile = UserProfile.objects.create(user=new_user)
            user_profile.user_role = 'USER_CUSTOMER'
            default_file_path = 'users/defaultProfilePic.jpg'
            user_profile.photo = default_file_path
            return render(request,
                          'account/register_done.html', {'new_user': new_user, })
    else:
        user_form = UserRegistrationForm()
        return render(request, 'account/user_register.html', {'user_form': user_form})


def shop_register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            # Save the User Object
            new_user.save()
            # create the user profile
            shop = ShopProfile.objects.create(user=new_user)
            shop.shop_name = request.POST['shop_name']
            shop.shop_address = request.POST['shop_address']
            shop.shop_contact = request.POST['shop_contact']
            shop.save()
            return redirect('login')
    else:
        user_form = UserRegistrationForm()
        shop_profile_form = ShopProfileCreationForm()
        return render(request, 'account/shop_register.html', {'user_form': user_form, 'shop_profile': shop_profile_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = UserProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully")
        else:
            messages.error(request, "Error updating your Profile")
    else:
        user_form = UserRegistrationForm(instance=request.user)
        profile_form = UserProfileEditForm(instance=request.user.profile)

    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


def test_function(input):
    pass