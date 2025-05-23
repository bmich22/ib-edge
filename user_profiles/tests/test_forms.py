from django.test import TestCase
from user_profiles import UserProfileForm


class UserProfileFormTest(TestCase):
    def test_valid_form_data(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'grade_year': 'IB2',
            'parent_email': 'parent@example.com',
        }
        form = UserProfileForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_email_format(self):
        form_data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'grade_year': '11',
            'parent_email': 'invalid-email',
        }
        form = UserProfileForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('parent_email', form.errors)
