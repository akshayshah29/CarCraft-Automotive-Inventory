from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Vehicle, Brand, VehicleEnquiry, VehicleWishlist


def vehicle_list_view(request):
    vehicles = Vehicle.objects.all()
    brands = Brand.objects.all()

    # Search query
    q = request.GET.get('q', '').strip()
    if q:
        vehicles = vehicles.filter(
            Q(model_name__icontains=q) |
            Q(brand__name__icontains=q) |
            Q(description__icontains=q) |
            Q(color__icontains=q) |
            Q(vin__icontains=q)
        )

    # Filter: Brand
    selected_brand = request.GET.get('brand')
    if selected_brand:
        vehicles = vehicles.filter(brand__slug=selected_brand)

    # Filter: Fuel Type
    selected_fuel = request.GET.get('fuel')
    if selected_fuel:
        vehicles = vehicles.filter(fuel_type=selected_fuel)

    # Filter: Transmission
    selected_transmission = request.GET.get('transmission')
    if selected_transmission:
        vehicles = vehicles.filter(transmission=selected_transmission)

    # Filter: Body Type
    selected_body = request.GET.get('body_type')
    if selected_body:
        vehicles = vehicles.filter(body_type=selected_body)

    # Filter: Availability
    selected_availability = request.GET.get('availability')
    if selected_availability:
        vehicles = vehicles.filter(availability=selected_availability)

    # Filter: Year
    min_year = request.GET.get('min_year')
    if min_year and min_year.isdigit():
        vehicles = vehicles.filter(year__gte=int(min_year))

    # Filter: Price
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price and min_price.isdigit():
        vehicles = vehicles.filter(price__gte=int(min_price))
    if max_price and max_price.isdigit():
        vehicles = vehicles.filter(price__lte=int(max_price))

    # Sorting
    sort = request.GET.get('sort', 'featured')
    if sort == 'price_asc':
        vehicles = vehicles.order_by('price')
    elif sort == 'price_desc':
        vehicles = vehicles.order_by('-price')
    elif sort == 'newest':
        vehicles = vehicles.order_by('-year', '-created_at')
    elif sort == 'oldest':
        vehicles = vehicles.order_by('year', 'created_at')
    elif sort == 'mileage_asc':
        vehicles = vehicles.order_by('mileage')
    else:
        vehicles = vehicles.order_by('-is_featured', '-created_at')

    # Get user wishlisted vehicle IDs
    user_wishlist_ids = []
    if request.user.is_authenticated:
        user_wishlist_ids = list(VehicleWishlist.objects.filter(user=request.user).values_list('vehicle_id', flat=True))

    # Pagination: 9 per page
    paginator = Paginator(vehicles, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Distinct values for filter dropdowns
    available_years = Vehicle.objects.values_list('year', flat=True).distinct().order_by('-year')

    context = {
        'page_obj': page_obj,
        'vehicles': page_obj.object_list,
        'brands': brands,
        'total_count': vehicles.count(),
        'available_years': available_years,
        'user_wishlist_ids': user_wishlist_ids,
        'current_filters': {
            'q': q,
            'brand': selected_brand or '',
            'fuel': selected_fuel or '',
            'transmission': selected_transmission or '',
            'body_type': selected_body or '',
            'availability': selected_availability or '',
            'min_year': min_year or '',
            'min_price': min_price or '',
            'max_price': max_price or '',
            'sort': sort,
        }
    }
    return render(request, 'vehicles/vehicle_list.html', context)


def vehicle_detail_view(request, slug):
    vehicle = get_object_or_404(Vehicle, slug=slug)
    related_vehicles = Vehicle.objects.filter(brand=vehicle.brand).exclude(pk=vehicle.pk)[:3]
    if not related_vehicles.exists():
        related_vehicles = Vehicle.objects.exclude(pk=vehicle.pk)[:3]

    is_wishlisted = False
    if request.user.is_authenticated:
        is_wishlisted = VehicleWishlist.objects.filter(user=request.user, vehicle=vehicle).exists()

    # Handle Enquiry Form submission
    if request.method == 'POST' and 'submit_enquiry' in request.POST:
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        message = request.POST.get('message', '').strip()
        preferred_contact = request.POST.get('preferred_contact', 'Phone')

        if name and email and phone:
            VehicleEnquiry.objects.create(
                vehicle=vehicle,
                name=name,
                email=email,
                phone=phone,
                message=message or f"I am interested in this {vehicle.year} {vehicle.title}.",
                preferred_contact=preferred_contact
            )
            messages.success(request, f"Thank you, {name}! Your enquiry for the {vehicle.title} has been received. Our luxury sales concierge will reach out via {preferred_contact} shortly.")
            return redirect('vehicles:detail', slug=vehicle.slug)
        else:
            messages.error(request, "Please fill in all required enquiry fields.")

    context = {
        'vehicle': vehicle,
        'gallery_images': vehicle.gallery_images.all(),
        'related_vehicles': related_vehicles,
        'is_wishlisted': is_wishlisted,
    }
    return render(request, 'vehicles/vehicle_detail.html', context)


@login_required
def toggle_vehicle_wishlist_view(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    wishlist_item = VehicleWishlist.objects.filter(user=request.user, vehicle=vehicle)
    
    if wishlist_item.exists():
        wishlist_item.delete()
        added = False
        msg = f"{vehicle.title} removed from your wishlist."
    else:
        VehicleWishlist.objects.create(user=request.user, vehicle=vehicle)
        added = True
        msg = f"{vehicle.title} added to your wishlist."

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        from products.models import ProductWishlist
        total_count = VehicleWishlist.objects.filter(user=request.user).count() + ProductWishlist.objects.filter(user=request.user).count()
        return JsonResponse({'success': True, 'added': added, 'message': msg, 'wishlist_count': total_count})

    messages.info(request, msg)
    next_url = request.META.get('HTTP_REFERER', 'vehicles:list')
    return redirect(next_url)
