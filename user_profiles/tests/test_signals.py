from django.test import TestCase
from django.contrib.auth.models import User
from user_profiles.models import UserProfile


class UserProfileSignalTests(TestCase):
    def test_profile_created_on_user_creation(self):
        user = User.objects.create_user(username='signaluser', password='pass123')
        profile = UserProfile.objects.get(user=user)
        self.assertEqual(profile.user, user)

    def test_profile_saved_on_user_update(self):
        user = User.objects.create_user(username='signalupdate', password='pass123')
        profile = user.userprofile
        original_id = profile.id

        # Trigger post_save on User by changing and saving the user
        user.first_name = "Updated"
        user.save()

        updated_profile = UserProfile.objects.get(user=user)
        self.assertEqual(updated_profile.id, original_id)  # Still the same profile
