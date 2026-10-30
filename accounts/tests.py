from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class AccountsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testdriver',
            email='testdriver@example.com',
            password='testpassword123',
            first_name='Jordan',
            last_name='Cole'
        )

    def test_registration_view(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)

        post_data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'phone': '+91 98765 43211',
            'password': 'password123',
            'confirm_password': 'password123',
        }
        res = self.client.post(reverse('accounts:register'), post_data)
        self.assertEqual(res.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_and_logout(self):
        res = self.client.post(reverse('accounts:login'), {
            'username': 'testdriver',
            'password': 'testpassword123',
        })
        self.assertEqual(res.status_code, 302)

        res_profile = self.client.get(reverse('accounts:profile'))
        self.assertEqual(res_profile.status_code, 200)
        self.assertContains(res_profile, 'Jordan Cole')

        res_logout = self.client.get(reverse('accounts:logout'))
        self.assertEqual(res_logout.status_code, 302)

    def test_about_page(self):
        res = self.client.get(reverse('about'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'About CarCraft')
        self.assertContains(res, 'Our Story')
        self.assertContains(res, 'Our Values')
        self.assertNotContains(res, 'Meet the Team')
        self.assertNotContains(res, 'THE EXPERTS')

    def test_contact_page_get(self):
        res = self.client.get(reverse('contact'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Get In Touch')
        self.assertContains(res, 'Send Message')
        self.assertContains(res, '+91 98765 43210')
        self.assertContains(res, 'Sector 62, Noida')

    def test_contact_page_post(self):
        from accounts.models import ContactMessage
        post_data = {
            'name': 'Alex Mercer',
            'email': 'alex@example.com',
            'phone': '+91 98765 43212',
            'subject': 'Vehicle Purchase Inquiry',
            'message': 'I would like to inquire about the BMW 330i availability.',
        }
        res = self.client.post(reverse('contact'), post_data)
        self.assertEqual(res.status_code, 302)
        self.assertTrue(ContactMessage.objects.filter(email='alex@example.com').exists())
        msg = ContactMessage.objects.get(email='alex@example.com')
        self.assertEqual(msg.name, 'Alex Mercer')
        self.assertEqual(msg.subject, 'Vehicle Purchase Inquiry')
        self.assertFalse(msg.is_read)
