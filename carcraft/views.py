from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from vehicles.models import Vehicle, Brand, VehicleWishlist
from products.models import Product, ProductCategory, ProductWishlist
from services.models import Service, Appointment
from orders.models import Order


def home_view(request):
    featured_vehicles = Vehicle.objects.filter(is_featured=True)[:6]
    if not featured_vehicles.exists():
        featured_vehicles = Vehicle.objects.all()[:6]

    featured_products = Product.objects.filter(is_featured=True)[:8]
    if not featured_products.exists():
        featured_products = Product.objects.all()[:8]

    services = Service.objects.all()[:8]
    brands = Brand.objects.all()[:8]

    user_vehicle_wishlist_ids = []
    user_product_wishlist_ids = []
    if request.user.is_authenticated:
        user_vehicle_wishlist_ids = list(VehicleWishlist.objects.filter(user=request.user).values_list('vehicle_id', flat=True))
        user_product_wishlist_ids = list(ProductWishlist.objects.filter(user=request.user).values_list('product_id', flat=True))

    context = {
        'featured_vehicles': featured_vehicles,
        'featured_products': featured_products,
        'services': services,
        'brands': brands,
        'user_vehicle_wishlist_ids': user_vehicle_wishlist_ids,
        'user_product_wishlist_ids': user_product_wishlist_ids,
    }
    return render(request, 'home.html', context)


def global_search_view(request):
    q = request.GET.get('q', '').strip()
    vehicles = []
    products = []
    services = []

    if q:
        vehicles = Vehicle.objects.filter(
            Q(model_name__icontains=q) |
            Q(brand__name__icontains=q) |
            Q(description__icontains=q) |
            Q(fuel_type__icontains=q) |
            Q(body_type__icontains=q)
        )[:10]

        products = Product.objects.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q) |
            Q(part_number__icontains=q) |
            Q(category__name__icontains=q)
        )[:10]

        services = Service.objects.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q) |
            Q(tagline__icontains=q)
        )[:10]

    context = {
        'q': q,
        'vehicles': vehicles,
        'products': products,
        'services': services,
        'total_results': len(vehicles) + len(products) + len(services),
    }
    return render(request, 'search_results.html', context)


@login_required
def wishlist_view(request):
    vehicle_wishlists = VehicleWishlist.objects.filter(user=request.user).select_related('vehicle', 'vehicle__brand')
    product_wishlists = ProductWishlist.objects.filter(user=request.user).select_related('product', 'product__category')

    context = {
        'vehicle_wishlists': vehicle_wishlists,
        'product_wishlists': product_wishlists,
        'total_count': vehicle_wishlists.count() + product_wishlists.count(),
    }
    return render(request, 'wishlist.html', context)


@login_required
def staff_dashboard_view(request):
    # Only staff/superusers can access the management dashboard
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('accounts:profile')

    total_vehicles = Vehicle.objects.count()
    available_vehicles = Vehicle.objects.filter(availability='Available').count()
    total_products = Product.objects.count()
    pending_orders = Order.objects.filter(status__in=['Pending', 'Confirmed']).count()
    pending_appointments = Appointment.objects.filter(status='Pending').count()
    registered_users = User.objects.count()

    recent_orders = Order.objects.all().order_by('-created_at')[:6]
    recent_appointments = Appointment.objects.all().order_by('-created_at')[:6]
    recent_vehicles = Vehicle.objects.all().order_by('-created_at')[:5]
    low_stock_products = Product.objects.filter(stock__lte=10).order_by('stock')[:6]

    context = {
        'total_vehicles': total_vehicles,
        'available_vehicles': available_vehicles,
        'total_products': total_products,
        'pending_orders': pending_orders,
        'pending_appointments': pending_appointments,
        'registered_users': registered_users,
        'recent_orders': recent_orders,
        'recent_appointments': recent_appointments,
        'recent_vehicles': recent_vehicles,
        'low_stock_products': low_stock_products,
    }
    return render(request, 'admin/dashboard.html', context)


@login_required
def staff_update_order_status(request, order_number):
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('accounts:profile')
    
    from django.shortcuts import get_object_or_404
    from django.contrib import messages
    order = get_object_or_404(Order, order_number=order_number)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, f"Order #{order.order_number} status updated to '{new_status}'.")
    return redirect('dashboard')


@login_required
def staff_update_appointment_status(request, appointment_id):
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('accounts:profile')

    from django.shortcuts import get_object_or_404
    from django.contrib import messages
    appointment = get_object_or_404(Appointment, appointment_id=appointment_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Appointment.STATUS_CHOICES):
            appointment.status = new_status
            appointment.save()
            messages.success(request, f"Appointment #{appointment.appointment_id} status updated to '{new_status}'.")
    return redirect('dashboard')


def handler404(request, exception):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)


def about_view(request):
    return render(request, 'about.html')


def contact_view(request):
    from accounts.models import ContactMessage
    from django.contrib import messages as django_messages
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        
        if name and email and subject and message:
            ContactMessage.objects.create(
                name=name, email=email, phone=phone,
                subject=subject, message=message
            )
            django_messages.success(request, 'Thank you for contacting CarCraft! We will get back to you shortly.')
            return redirect('contact')
        else:
            django_messages.error(request, 'Please fill in all required fields.')
    
    return render(request, 'contact.html')

