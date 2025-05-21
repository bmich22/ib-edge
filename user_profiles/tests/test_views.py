from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from user_profiles.models import UserProfile


class UserProfileViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_student_sees_user_profile_template(self):
        student = User.objects.create_user(username='student', password='pass123')
        self.client.login(username='student', password='pass123')
        response = self.client.get(reverse('user_profile'))
        self.assertTemplateUsed(response, 'user_profiles/user_profile.html')

    def test_tutor_sees_tutor_dashboard_template(self):
        tutor = User.objects.create_user(username='tutor', password='pass123')
        tutor.userprofile.is_tutor = True
        tutor.userprofile.save()
        self.client.login(username='tutor', password='pass123')
        response = self.client.get(reverse('user_profile'))
        self.assertTemplateUsed(response, 'user_profiles/tutor_dashboard.html')

    def test_admin_sees_admin_dashboard_template(self):
        admin = User.objects.create_superuser(username='admin', password='pass123', email='admin@example.com')
        self.client.login(username='admin', password='pass123')
        response = self.client.get(reverse('user_profile'))
        self.assertTemplateUsed(response, 'user_profiles/admin_dashboard.html')

    def test_profile_auto_created_with_user(self):
        user = User.objects.create_user(username='newuser', password='pass123')
        self.assertTrue(UserProfile.objects.filter(user=user).exists())

    def test_profile_form_updates_data(self):
        user = User.objects.create_user(username='formuser', password='pass123')
        self.client.login(username='formuser', password='pass123')

        update_data = {
            'first_name': 'Updated',
            'last_name': 'User',
            'grade_year': '11',
            'parent_email': 'parent@example.com',
        }

        response = self.client.post(reverse('user_profile'), data=update_data)
        self.assertRedirects(response, reverse('user_profile'))  # on success, it redirects

        profile = UserProfile.objects.get(user=user)
        self.assertEqual(profile.first_name, 'Updated')
        self.assertEqual(profile.last_name, 'User')
        self.assertEqual(profile.grade_year, '11')
        self.assertEqual(profile.parent_email, 'parent@example.com')