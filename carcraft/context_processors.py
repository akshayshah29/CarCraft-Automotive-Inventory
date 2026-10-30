def global_context(request):
    """
    Context processor to inject dynamic site-wide variables:
    Cart items count, wishlist count, vehicle brands, product categories.
    """
    context = {
        'cart_count': 0,
        'wishlist_count': 0,
        'nav_brands': [],
        'nav_categories': [],
    }

    try:
        # Wishlist count for authenticated users
        if request.user.is_authenticated:
            from vehicles.models import VehicleWishlist
            from products.models import ProductWishlist
            v_count = VehicleWishlist.objects.filter(user=request.user).count()
            p_count = ProductWishlist.objects.filter(user=request.user).count()
            context['wishlist_count'] = v_count + p_count

        # Cart item count
        from orders.models import Cart
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
        else:
            session_key = request.session.session_key
            if not session_key:
                # Do not force session creation here unless needed
                cart = None
            else:
                cart = Cart.objects.filter(session_key=session_key).first()

        if cart:
            context['cart_count'] = cart.total_items
            context['cart_subtotal'] = cart.subtotal
    except Exception:
        # Fails gracefully during initial migrations or empty DB
        pass

    try:
        from vehicles.models import Brand
        from products.models import ProductCategory
        context['nav_brands'] = Brand.objects.all()[:6]
        context['nav_categories'] = ProductCategory.objects.all()[:8]
    except Exception:
        pass

    return context
