from django.test import TestCase
from django.contrib.auth.models import User
from checkout.models import Purchase
from packages.models import Package
from user_profiles.models import Subject


class PurchaseModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='buyer', password='pass123')
        self.package = Package.objects.create(
            name='Pro', description='Advanced', price=150.0, num_sessions=10
        )
        self.subject = Subject.objects.create(name='English')

    def test_purchase_str_repr(self):
        purchase = Purchase.objects.create(
            user=self.user,
            package=self.package,
            subject_choice=self.subject,
            customer_email='parent@example.com'
        )
        expected = f"{self.user.username} – {self.package.name}"
        self.assertEqual(str(purchase), expected)

    def test_sessions_remaining(self):
        purchase = Purchase.objects.create(
            user=self.user,
            package=self.package,
            subject_choice=self.subject,
            customer_email='parent@example.com'
        )
        # Simulate that 3 sessions have been used
        purchase.sessions_used = 3
        self.assertEqual(purchase.sessions_remaining(), 7)

    def test_sessions_remaining_no_package(self):
        purchase = Purchase.objects.create(
            user=self.user,
            package=None,
            subject_choice=self.subject,
            customer_email='parent@example.com'
        )
        purchase.sessions_used = 2
        self.assertEqual(purchase.sessions_remaining(), 0)