from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import ProductCategory, Product, ProductWishlist


class ProductsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='partbuyer', password='password123')
        self.cat = ProductCategory.objects.create(name='Brake Parts')
        self.product = Product.objects.create(
            category=self.cat,
            name='Brembo Racing Pads',
            part_number='BRM-PAD-01',
            price=Decimal('150.00'),
            stock=10,
            description='High endurance racing pads.'
        )

    def test_product_list_and_category(self):
        res = self.client.get(reverse('products:list'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Brembo Racing Pads')

        res_cat = self.client.get(reverse('products:list'), {'category': self.cat.slug})
        self.assertEqual(res_cat.status_code, 200)
        self.assertContains(res_cat, 'Brembo Racing Pads')

    def test_product_detail(self):
        res = self.client.get(reverse('products:detail', kwargs={'slug': self.product.slug}))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'BRM-PAD-01')

    def test_product_wishlist_toggle(self):
        self.client.login(username='partbuyer', password='password123')
        res = self.client.post(reverse('products:wishlist_toggle', kwargs={'product_id': self.product.id}))
        self.assertTrue(ProductWishlist.objects.filter(user=self.user, product=self.product).exists())
