from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from products.models import Product
from .models import Cart, CartItem, Order, OrderItem


def _get_or_create_cart(request):
    """Helper to retrieve or initialize the user's or session's Cart."""
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart


def cart_detail_view(request):
    cart = _get_or_create_cart(request)
    items = cart.items.select_related('product', 'product__category').all()
    
    context = {
        'cart': cart,
        'items': items,
    }
    return render(request, 'orders/cart.html', context)


def add_to_cart_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = _get_or_create_cart(request)

    quantity = 1
    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
            if quantity < 1:
                quantity = 1
        except ValueError:
            quantity = 1

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()

    msg = f"Added {quantity}x {product.name} to your cart."
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': msg,
            'cart_count': cart.total_items,
            'cart_subtotal': float(cart.subtotal)
        })

    messages.success(request, msg)
    return redirect('orders:cart')


def update_cart_item_view(request, item_id):
    cart = _get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'increase':
            cart_item.quantity += 1
            cart_item.save()
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
        elif action == 'set':
            try:
                qty = int(request.POST.get('quantity', 1))
                if qty > 0:
                    cart_item.quantity = qty
                    cart_item.save()
                else:
                    cart_item.delete()
            except ValueError:
                pass

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': cart.total_items,
            'cart_subtotal': float(cart.subtotal),
            'cart_total': float(cart.total),
        })

    return redirect('orders:cart')


def remove_from_cart_view(request, item_id):
    cart = _get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    product_name = cart_item.product.name
    cart_item.delete()

    messages.info(request, f"Removed {product_name} from your cart.")
    return redirect('orders:cart')


def checkout_view(request):
    cart = _get_or_create_cart(request)
    items = cart.items.select_related('product').all()

    if not items.exists():
        messages.warning(request, "Your cart is currently empty. Add parts or accessories before proceeding to checkout.")
        return redirect('products:list')

    # Prefill form fields if user is authenticated
    initial_data = {}
    if request.user.is_authenticated:
        u = request.user
        initial_data['name'] = f"{u.first_name} {u.last_name}".strip() or u.username
        initial_data['email'] = u.email
        if hasattr(u, 'profile'):
            p = u.profile
            initial_data['phone'] = p.phone or ''
            initial_data['address'] = p.address or ''
            initial_data['city'] = p.city or ''
            initial_data['state'] = p.state or ''
            initial_data['pincode'] = p.pincode or ''

    if request.method == 'POST':
        full_name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip()
        pincode = request.POST.get('pincode', '').strip()

        if not (full_name and email and phone and address and city and state and pincode):
            messages.error(request, "Please fill in all required shipping and contact fields.")
        else:
            # Create Order
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                full_name=full_name,
                email=email,
                phone=phone,
                address=address,
                city=city,
                state=state,
                pincode=pincode,
                subtotal=cart.subtotal,
                tax=cart.estimated_tax,
                shipping_cost=0.00,
                total_amount=cart.total,
                status='Confirmed',
                payment_method='Simulated Payment Gateway (Academic Demo)',
                payment_status='Paid'
            )

            # Create OrderItems and decrement stock
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    product_name=item.product.name,
                    price=item.product.price,
                    quantity=item.quantity
                )
                if item.product.stock >= item.quantity:
                    item.product.stock -= item.quantity
                    item.product.save()

            # Empty Cart
            cart.items.all().delete()

            messages.success(request, f"Order #{order.order_number} confirmed! Thank you for choosing CarCraft.")
            return redirect('orders:confirmation', order_number=order.order_number)

    context = {
        'cart': cart,
        'items': items,
        'initial': initial_data,
    }
    return render(request, 'orders/checkout.html', context)


def order_confirmation_view(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    context = {
        'order': order,
        'items': order.items.select_related('product').all()
    }
    return render(request, 'orders/order_confirmation.html', context)


@login_required
def order_history_view(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_history.html', {'orders': orders})


@login_required
def order_detail_view(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'orders/order_detail.html', {
        'order': order,
        'items': order.items.all()
    })
