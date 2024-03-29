from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import (
    LoginForm,
    UserEditForm,
    UserRegistrationForm,
    UserProfileEditForm,
    ShopProfileCreationForm)

from ovros_payment_module.forms import ShopBankDetAddForm
from ovros_payment_module.models import ShopPaymentDetail

from .models import (
    UserProfile,
    ShopProfile)
from django.contrib import messages
from .profile_detail import ProfileData

# Create your views here.


def user_login(request):
    """
    User login
    :param request:
    :return:
    """
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
    """
    Redirect users to specified dashboard
    :param request:
    :return:
    """
    #print('session data : ', request.session.keys())
    #print('is_super user ', request.user.is_superuser)
    if not request.user.is_superuser:
        try:
            user_profile = UserProfile.objects.get(user_id=request.user.id)
        except UserProfile.DoesNotExist:
            user_profile = ShopProfile.objects.get(user_id=request.user.id)

        profile_data = ProfileData(request)

        if user_profile.user_role == "USER_CUSTOMER":
            profile_data.add(request.user.id, user_profile.id, 'USER_CUSTOMER')
            return redirect('user_overview')

        if user_profile.user_role == "USER_ADMIN":
            profile_data.add(request.user.id, user_profile.id, 'USER_ADMIN')
            return redirect('admin:login')

        if user_profile.user_role == "USER_SHOP":
            profile_data.add(request.user.id, user_profile.id, 'USER_SHOP')
            return redirect('shop_overview')
    else:
        return redirect('admin:login')


def register(request):
    """
    Render register page (landing page for registration)
    :param request:
    :return:
    """
    return render(request, 'account/register.html')


def user_register(request):
    """
    User registration
    :param request:
    :return:
    """
    print("User reg start")
    if request.method == 'POST':
        print("User reg inside post")
        user_form = UserRegistrationForm(request.POST)
        user_profile_form = UserProfileEditForm(data=request.POST, files=request.FILES or None)
        if user_form.is_valid() and user_profile_form.is_valid():
            # create a new user object but avoid saving it yet
            profile_cd = user_profile_form.cleaned_data
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
            #default_file_path = 'users/defaultProfilePic.jpg'
            #user_profile.photo = default_file_path
            messages.success(request, "User Registration Success")
            user_profile.photo = profile_cd['photo']
            user_profile.contact_number = profile_cd['contact_number']
            user_profile.save()
            print("User reg success ")
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
        else:
            print("User reg failed")
            messages.error(request, "User Registration Failed")
            return render(request, 'account/user_register.html',
                          {'user_form': user_form,
                           'user_profile_form': user_profile_form})
    elif request.method == "GET":
        print("User reg GET, started")
        user_form = UserRegistrationForm()
        user_profile_form = UserProfileEditForm()
        return render(request, 'account/user_register.html',
                      {'user_form': user_form,
                       'user_profile_form': user_profile_form})


def shop_register(request):
    """
    Shop registration
    :param request:
    :return:
    """
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        shop_profile_form = ShopProfileCreationForm(request.POST)
        shop_bank_detail_form = ShopBankDetAddForm(request.POST)
        if user_form.is_valid() and shop_profile_form.is_valid() and shop_bank_detail_form.is_valid():
            # create a new user object but avoid saving it yet
            shop_p_cd = shop_profile_form.cleaned_data
            shop_bank_detail_cd = shop_bank_detail_form.cleaned_data
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
            shop.shop_address_no = request.POST['shop_address_no']
            shop.shop_address_street = request.POST['shop_address_street']
            shop.shop_address_city = request.POST['shop_address_city']
            if shop_p_cd['shop_profile_img']:
                shop.shop_profile_img = shop_p_cd['shop_profile_img']
            shop.shop_address_district = request.POST['shop_address_district']
            shop.shop_contact = request.POST['shop_contact']

            shop_p_details = ShopPaymentDetail.objects.create(shop_profile=shop)
            shop_p_details.bank_name = shop_bank_detail_cd['bank_name']
            shop_p_details.bank_branch = shop_bank_detail_cd['bank_branch']
            shop_p_details.account_name = shop_bank_detail_cd['account_name']
            shop_p_details.account_no = shop_bank_detail_cd['account_no']

            shop.save()
            shop_p_details.save()
            return redirect('login')
        else:
            return render(request, 'account/shop_register.html', {
                'user_form': user_form, ''
                'shop_profile': shop_profile_form,
                'shop_bank_detail_form': shop_bank_detail_form})
    else:
        intial_data = {
            "shop_address_no": " ",
            "shop_address_street": "",
            "shop_address_city": "",
            "shop_address_district": ""
        }
        user_form = UserRegistrationForm()
        shop_profile_form = ShopProfileCreationForm(initial=intial_data)
        shop_bank_detail_form = ShopBankDetAddForm()
        return render(request, 'account/shop_register.html', {
            'user_form': user_form,
            'shop_profile': shop_profile_form,
            'shop_bank_detail_form': shop_bank_detail_form
        })


@login_required
def edit(request):
    """
    Edit profile
    :param request:
    :return:
    """
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
