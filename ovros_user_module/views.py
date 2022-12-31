from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
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

# Create your views here.


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
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
    try:
        user_profile = UserProfile.objects.get(user_id=request.user.id)
    except UserProfile.DoesNotExist:
        user_profile = ShopProfile.objects.get(user_id=request.user.id)

    if user_profile.user_role == "USER_CUSTOMER":
        return render(request,
                      'ovros_dashboard/user_dashboard/user_dashboard.html',
                      {'section': 'dashboard', 'user_profile': user_profile.user_role})

    if user_profile.user_role == "USER_ADMIN":
        return render(request,
                      'ovros_dashboard/admin_dashboard/admin_dashboard_overview.html',
                      {'section': 'dashboard', 'user_profile': user_profile.user_role})

    if user_profile.user_role == "USER_SHOP":
        return render(request,
                      'ovros_dashboard/shop_dashboard/shop_dashboard.html',
                      {'section': 'dashboard', 'user_profile': user_profile.user_role})

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
            UserProfile.objects.create(user=new_user, user_role='USER_CUSTOMER')
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
            UserProfile.objects.create(user=new_user)
            return render(request,
                          'account/shop_register.html', {'new_user': new_user})
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

