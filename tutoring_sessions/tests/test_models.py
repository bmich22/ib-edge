from django.test import TestCase
from django.contrib.auth.models import User
from tutoring_sessions.models import TutoringSession
from datetime import datetime


class TutoringSessionModelTest(TestCase):
    def test_str_method(self):
        student = User.objects.create_user(
            username='student1', password='pass123')
        tutor = User.objects.create_user(
            username='tutor1', password='pass123')

        session = TutoringSession.objects.create(
            user=student,
            session_datetime=datetime(2025, 5, 21, 14, 0),
            notes='Reviewed past papers.',
            logged_by=tutor
        )

        expected = "student1 — May 21, 2025 02:00 PM"
        self.assertEqual(str(session), expected)
