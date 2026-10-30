from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Product, ProductCategory, ProductWishlist


def product_list_view(request):
    products = Product.objects.all()
    categories = ProductCategory.objects.all()

    # Search
    q = request.GET.get('q', '').strip()
    if q:
        products = products.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q) |
            Q(part_number__icontains=q) |
            Q(brand_compatibility__icontains=q)
        )

    # Filter: Category
    selected_category = request.GET.get('category')
    current_cat_obj = None
    if selected_category:
        products = products.filter(category__slug=selected_category)
        current_cat_obj = ProductCategory.objects.filter(slug=selected_category).first()

    # Filter: Price
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price and min_price.isdigit():
        products = products.filter(price__gte=int(min_price))
    if max_price and max_price.isdigit():
        products = products.filter(price__lte=int(max_price))

    # Filter: In Stock Only
    in_stock = request.GET.get('in_stock')
    if in_stock == '1':
        products = products.filter(stock__gt=0)

    # Sorting
    sort = request.GET.get('sort', 'featured')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'newest':
        products = products.order_by('-created_at')
    elif sort == 'name_asc':
        products = products.order_by('name')
    else:
        products = products.order_by('-is_featured', '-created_at')

    # Wishlist IDs for user
    user_wishlist_ids = []
    if request.user.is_authenticated:
        user_wishlist_ids = list(ProductWishlist.objects.filter(user=request.user).values_list('product_id', flat=True))

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'products': page_obj.object_list,
        'categories': categories,
        'current_category': current_cat_obj,
        'total_count': products.count(),
        'user_wishlist_ids': user_wishlist_ids,
        'current_filters': {
            'q': q,
            'category': selected_category or '',
            'min_price': min_price or '',
            'max_price': max_price or '',
            'in_stock': in_stock or '',
            'sort': sort,
        }
    }
    return render(request, 'products/product_list.html', context)


def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(pk=product.pk)[:4]

    is_wishlisted = False
    if request.user.is_authenticated:
        is_wishlisted = ProductWishlist.objects.filter(user=request.user, product=product).exists()

    context = {
        'product': product,
        'related_products': related_products,
        'is_wishlisted': is_wishlisted,
    }
    return render(request, 'products/product_detail.html', context)


@login_required
def toggle_product_wishlist_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item = ProductWishlist.objects.filter(user=request.user, product=product)

    if wishlist_item.exists():
        wishlist_item.delete()
        added = False
        msg = f"{product.name} removed from your wishlist."
    else:
        ProductWishlist.objects.create(user=request.user, product=product)
        added = True
        msg = f"{product.name} added to your wishlist."

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        from vehicles.models import VehicleWishlist
        total_count = ProductWishlist.objects.filter(user=request.user).count() + VehicleWishlist.objects.filter(user=request.user).count()
        return JsonResponse({'success': True, 'added': added, 'message': msg, 'wishlist_count': total_count})

    messages.info(request, msg)
    next_url = request.META.get('HTTP_REFERER', 'products:list')
    return redirect(next_url)
