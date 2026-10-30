import datetime
from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Service, Appointment


class ServicesTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='careowner', password='password123')
        self.service = Service.objects.create(
            name='Precision Oil Change',
            tagline='Synthetic engine lubricant upgrade',
            description='Factory synthetic oil replacement with OEM filter.',
            price=Decimal('2999.00'),
            duration='45 Minutes',
            what_is_included='Full synthetic oil\nOEM oil filter\nVisual safety inspection'
        )

    def test_service_list_and_detail(self):
        res = self.client.get(reverse('services:list'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Precision Oil Change')

        res_detail = self.client.get(reverse('services:detail', kwargs={'slug': self.service.slug}))
        self.assertEqual(res_detail.status_code, 200)
        self.assertContains(res_detail, 'Synthetic engine lubricant upgrade')

    def test_service_booking_and_confirmation(self):
        self.client.login(username='careowner', password='password123')
        booking_data = {
            'service_id': self.service.id,
            'vehicle_model': '2023 BMW M3',
            'vehicle_reg_number': 'DL-01-AB-1234',
            'preferred_date': (datetime.date.today() + datetime.timedelta(days=3)).isoformat(),
            'preferred_time': '11:00 AM - 01:00 PM',
            'customer_name': 'Care Owner',
            'customer_email': 'owner@example.com',
            'customer_phone': '+91 98765 43210',
            'notes': 'Please inspect brake pads as well.'
        }
        res_book = self.client.post(reverse('services:book'), booking_data)
        self.assertEqual(res_book.status_code, 302)

        appt = Appointment.objects.filter(user=self.user).first()
        self.assertIsNotNone(appt)
        self.assertEqual(appt.vehicle_model, '2023 BMW M3')
        self.assertEqual(appt.status, 'Pending')

        # Confirmation view
        res_conf = self.client.get(reverse('services:confirmation', kwargs={'appointment_id': appt.appointment_id}))
        self.assertEqual(res_conf.status_code, 200)
        self.assertContains(res_conf, appt.appointment_id)

        # History view
        res_hist = self.client.get(reverse('services:history'))
        self.assertEqual(res_hist.status_code, 200)
        self.assertContains(res_hist, appt.appointment_id)
