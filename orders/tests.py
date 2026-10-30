from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import ProductCategory, Product
from .models import Cart, CartItem, Order, OrderItem


class OrdersTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='shopper', email='shopper@example.com', password='password123')
        self.cat = ProductCategory.objects.create(name='Engine Parts')
        self.product = Product.objects.create(
            category=self.cat,
            name='KN High Flow Air Filter',
            part_number='KN-001',
            price=Decimal('7800.00'),
            stock=15,
            description='Washable high flow air filter.'
        )

    def test_cart_workflow(self):
        # 1. Add to cart
        res_add = self.client.post(reverse('orders:add_to_cart', kwargs={'product_id': self.product.id}), {'quantity': 2})
        self.assertEqual(res_add.status_code, 302)

        # 2. View cart
        res_cart = self.client.get(reverse('orders:cart'))
        self.assertEqual(res_cart.status_code, 200)
        self.assertContains(res_cart, 'KN High Flow Air Filter')
        self.assertContains(res_cart, '₹15,600')

        # 3. Update quantity
        cart = Cart.objects.first()
        cart_item = cart.items.first()
        res_upd = self.client.post(reverse('orders:update_cart_item', kwargs={'item_id': cart_item.id}), {'action': 'increase'})
        self.assertEqual(res_upd.status_code, 302)
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, 3)

    def test_checkout_and_order_creation(self):
        self.client.login(username='shopper', password='password123')
        self.client.post(reverse('orders:add_to_cart', kwargs={'product_id': self.product.id}), {'quantity': 1})

        checkout_data = {
            'name': 'Test Shopper',
            'email': 'shopper@example.com',
            'phone': '+91 98765 43210',
            'address': 'Sector 62, Noida',
            'city': 'Noida',
            'state': 'Uttar Pradesh',
            'pincode': '201309',
        }
        res_checkout = self.client.post(reverse('orders:checkout'), checkout_data)
        self.assertEqual(res_checkout.status_code, 302)

        order = Order.objects.filter(user=self.user).first()
        self.assertIsNotNone(order)
        self.assertEqual(order.full_name, 'Test Shopper')
        self.assertEqual(order.status, 'Confirmed')

        # Order history
        res_hist = self.client.get(reverse('orders:history'))
        self.assertEqual(res_hist.status_code, 200)
        self.assertContains(res_hist, order.order_number)
