from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Brand, Vehicle, VehicleWishlist, VehicleEnquiry


class VehiclesTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='carfan', password='password123')
        self.brand = Brand.objects.create(name='BMW', country='Germany')
        self.vehicle = Vehicle.objects.create(
            brand=self.brand,
            model_name='M3 Competition',
            year=2024,
            price=Decimal('12500000.00'),
            fuel_type='Petrol',
            transmission='Automatic',
            body_type='Sedan',
            mileage=5000,
            engine_capacity='3.0L Twin-Turbo',
            horsepower=503,
            vin='WBA3M3COMP202409',
            availability='Available',
            is_featured=True,
            description='Ultimate driving machine in pristine condition.'
        )

    def test_vehicle_list_and_filters(self):
        res = self.client.get(reverse('vehicles:list'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'M3 Competition')

        # Filter by brand
        res_filter = self.client.get(reverse('vehicles:list'), {'brand': 'bmw'})
        self.assertEqual(res_filter.status_code, 200)
        self.assertContains(res_filter, 'M3 Competition')

        # Filter by fuel
        res_fuel = self.client.get(reverse('vehicles:list'), {'fuel': 'Electric'})
        self.assertEqual(res_fuel.status_code, 200)
        self.assertNotContains(res_fuel, 'M3 Competition')

    def test_vehicle_detail_and_enquiry(self):
        res = self.client.get(reverse('vehicles:detail', kwargs={'slug': self.vehicle.slug}))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'WBA3M3COMP202409')
        self.assertContains(res, '₹1,25,00,000')
        self.assertContains(res, 'cc-specs-table')
        self.assertContains(res, 'Key Specifications')
        self.assertContains(res, 'cc-spec-label')
        self.assertContains(res, 'cc-spec-value')

        # Post enquiry
        post_data = {
            'submit_enquiry': '1',
            'name': 'Test Buyer',
            'email': 'buyer@example.com',
            'phone': '+91 98765 43210',
            'preferred_contact': 'Phone',
            'message': 'Interested in a test drive.'
        }
        res_enquiry = self.client.post(reverse('vehicles:detail', kwargs={'slug': self.vehicle.slug}), post_data)
        self.assertEqual(res_enquiry.status_code, 302)
        self.assertTrue(VehicleEnquiry.objects.filter(vehicle=self.vehicle, email='buyer@example.com').exists())

    def test_vehicle_wishlist_toggle(self):
        self.client.login(username='carfan', password='password123')
        res = self.client.post(reverse('vehicles:wishlist_toggle', kwargs={'vehicle_id': self.vehicle.id}))
        self.assertTrue(VehicleWishlist.objects.filter(user=self.user, vehicle=self.vehicle).exists())

        # Toggle again to remove
        res2 = self.client.post(reverse('vehicles:wishlist_toggle', kwargs={'vehicle_id': self.vehicle.id}))
        self.assertFalse(VehicleWishlist.objects.filter(user=self.user, vehicle=self.vehicle).exists())
