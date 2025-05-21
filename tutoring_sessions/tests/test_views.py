from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from user_profiles.models import UserProfile
from tutoring_sessions.models import TutoringSession
from datetime import date
from checkout.models import Purchase
from packages.models import Package
from user_profiles.models import Subject


class TutoringSessionViewTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.subject = Subject.objects.create(name='Math')
        self.package = Package.objects.create(
            name='Basic', description='...', price=50.0, num_sessions=5
        )

        self.student_user = User.objects.create_user(username='student1', password='pass123')
        self.student_profile = self.student_user.userprofile
        self.student_profile.total_sessions_available = 3
        self.student_profile.save()

        # Create a valid purchase for the student so they pass the form filter
        Purchase.objects.create(
            user=self.student_user,
            package=self.package,
            customer_email='parent@example.com',
            subject_choice=self.subject
        )

        self.tutor_user = User.objects.create_user(username='tutor1', password='pass123')
        self.tutor_profile = self.tutor_user.userprofile
        self.tutor_profile.is_tutor = True
        self.tutor_profile.save()

    def test_log_session_requires_login(self):
        response = self.client.get(reverse('log_tutoring_session'))
        self.assertEqual(response.status_code, 302)  # Redirect to login page

    def test_log_session_blocks_non_tutor(self):
        self.client.login(username='student1', password='pass123')
        response = self.client.get(reverse('log_tutoring_session'))
        self.assertEqual(response.status_code, 403)

    def test_log_session_saves_valid_data(self):
        self.client.login(username='tutor1', password='pass123')

        post_data = {
            'student': self.student_profile.id,  # Use .id for ModelChoiceField
            'session_date': date.today().isoformat(),
            'session_time': '14:00:00',
            'notes': 'Great session on calculus.'
        }

        response = self.client.post(reverse('log_tutoring_session'), data=post_data)
        self.assertEqual(response.status_code, 302)  # Expect redirect on success

        session = TutoringSession.objects.first()
        self.assertIsNotNone(session)
        self.assertEqual(session.user, self.student_user)
        self.assertEqual(session.logged_by, self.tutor_user)
        self.assertEqual(session.notes, 'Great session on calculus.')

    def test_session_decrements_student_count(self):
        self.client.login(username='tutor1', password='pass123')

        pre_count = self.student_profile.total_sessions_available

        post_data = {
            'student': self.student_profile.id,
            'session_date': date.today().isoformat(),
            'session_time': '14:00:00',
            'notes': 'Test decrement.'
        }

        response = self.client.post(reverse('log_tutoring_session'), data=post_data)
        self.assertEqual(response.status_code, 302)

        self.student_profile.refresh_from_db()
        self.assertEqual(self.student_profile.total_sessions_available, pre_count - 1)
