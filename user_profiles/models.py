from django.db import models
from django.contrib.auth.models import User
from checkout.models import Purchase
from tutoring_sessions.models import TutoringSession
from django.db.models import Sum

# Create your models here.


# Tutoring subjects like "Math HL", "English SL"
class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # All users
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)

    # Students
    grade_year = models.CharField(
        max_length=20, blank=True)  # Example: "11", "IB2"
    parent_email = models.EmailField(blank=True, null=True)
    subjects = models.ManyToManyField('Subject', blank=True)
    total_sessions_available = models.PositiveIntegerField(default=0)

    # Tutor-specific
    is_tutor = models.BooleanField(default=False)
    bio = models.TextField(blank=True)
    calendly_url = models.URLField(blank=True)

    def __str__(self):
        return self.user.username

    def get_total_sessions_available(self):
        total_purchased = Purchase.objects.filter(user=self.user).aggregate(
            total=Sum('package__num_sessions')
        )['total'] or 0

        total_logged = TutoringSession.objects.filter(user=self.user).count()

        return max(0, total_purchased - total_logged)
