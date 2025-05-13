from django.apps import AppConfig


class UserProfilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_profiles'
    verbose_name = '1. User Management'

    def ready(self):
        import user_profiles.signals
    
