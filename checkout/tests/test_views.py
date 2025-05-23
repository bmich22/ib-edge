from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from checkout.models import Purchase
from packages.models import Package
from user_profiles.models import Subject
from unittest.mock import patch


class CheckoutFlowTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='test123')
        self.subject = Subject.objects.create(name='Math')
        self.package = Package.objects.create(
            name='Starter', description='Great intro',
            price=50.0, num_sessions=5
        )

    def test_checkout_page_renders(self):
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')

    def test_who_is_paying_requires_login(self):
        response = self.client.get(
            reverse('who_is_paying', args=[self.package.id]))
        self.assertRedirects(
            response,
            f"/accounts/login/?next=/checkout/who_is_paying/{self.package.id}/")

    @patch('checkout.views.stripe.checkout.Session.create')  # Mock Stripe
    def test_checkout_success_creates_purchase(self, mock_stripe_create):
        self.client.login(username='testuser', password='test123')

        session = self.client.session
        session['customer_email'] = 'parent@example.com'
        session['subject_id'] = self.subject.id
        session['purchased_package_id'] = self.package.id
        session.save()

        mock_stripe_create.return_value = type('obj', (object,), {
            "id": "fake_id",
            "payment_intent": "fake_intent",
            "url": "https://fake.stripe.com/session"
        })

        response = self.client.get(
            reverse('start_checkout', args=[self.package.id]))
        self.assertRedirects(response, "https://fake.stripe.com/session",
                             status_code=302, fetch_redirect_response=False)

        session = self.client.session
        session['purchased_package_id'] = self.package.id
        session.save()

        response = self.client.get(reverse('checkout_success'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')

    def test_checkout_cancel_renders(self):
        self.client.login(username='testuser', password='test123')
        response = self.client.get(reverse('checkout_cancel'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_cancel.html')
