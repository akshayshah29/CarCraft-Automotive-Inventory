from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm, UserUpdateForm, ProfileUpdateForm
from orders.models import Order
from services.models import Appointment
from vehicles.models import VehicleWishlist
from products.models import ProductWishlist


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            phone = form.cleaned_data.get('phone')
            if phone and hasattr(user, 'profile'):
                user.profile.phone = phone
                user.profile.save()

            messages.success(request, f"Welcome to CarCraft, {user.first_name or user.username}! Your account has been created.")
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('home')
        messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out of CarCraft.")
    return redirect('home')


@login_required
def profile_view(request):
    user = request.user
    recent_orders = Order.objects.filter(user=user)[:3]
    recent_appointments = Appointment.objects.filter(user=user)[:3]
    v_wishlist_count = VehicleWishlist.objects.filter(user=user).count()
    p_wishlist_count = ProductWishlist.objects.filter(user=user).count()
    
    context = {
        'user': user,
        'profile': getattr(user, 'profile', None),
        'recent_orders': recent_orders,
        'recent_appointments': recent_appointments,
        'wishlist_count': v_wishlist_count + p_wishlist_count,
        'orders_count': Order.objects.filter(user=user).count(),
        'appointments_count': Appointment.objects.filter(user=user).count(),
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def edit_profile_view(request):
    user = request.user
    profile = getattr(user, 'profile', None)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('accounts:profile')
        else:
            messages.error(request, "Please check the form for errors.")
    else:
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=profile)

    return render(request, 'accounts/edit_profile.html', {
        'u_form': u_form,
        'p_form': p_form
    })
