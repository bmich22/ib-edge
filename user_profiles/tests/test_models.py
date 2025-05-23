from datetime import datetime, timedelta
from django.contrib.auth.models import User
from user_profiles.models import UserProfile
from checkout.models import Purchase, Package
from tutoring_sessions.models import TutoringSession
from django.test import TestCase


class UserProfileMethodTest(TestCase):
    def setUp(self):
        # Create user and profile
        self.user = User.objects.create_user(
            username='student1', password='test123')
        self.profile = self.user.userprofile

        # Create a second user to act as the one who logs the sessions
        self.logger = User.objects.create_user(
            username='tutor1', password='pass456')

        # Create package and purchase
        self.package = Package.objects.create(
            name='Basic',
            num_sessions=5,
            price=100.0
        )
        Purchase.objects.create(user=self.user, package=self.package)

        # Create two tutoring sessions
        TutoringSession.objects.create(
            user=self.user,
            session_datetime=datetime.now() - timedelta(days=1),
            logged_by=self.logger
        )
        TutoringSession.objects.create(
            user=self.user,
            session_datetime=datetime.now() - timedelta(days=2),
            logged_by=self.logger
        )

    def test_get_total_sessions_available(self):
        available = self.profile.get_total_sessions_available()
        self.assertEqual(available, 3)  # 5 purchased - 2 logged
