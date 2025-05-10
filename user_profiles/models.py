from django.db import models
from django.contrib.auth.models import User
from packages.models import Package

# Create your models here.


# Tutoring subjects like "Math HL", "English SL"
class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    grade_year = models.CharField(max_length=20, blank=True)  # Example: "Year 11", "IB2"
    parent_email = models.EmailField(blank=True, null=True)
    package = models.ForeignKey(Package, on_delete=models.SET_NULL, null=True, blank=True)
    subjects = models.ManyToManyField('Subject', blank=True)
    package_assigned_date = models.DateTimeField(null=True, blank=True)
    sessions_used = models.PositiveIntegerField(default=0)

    def sessions_remaining(self):
        if self.package:
            return self.package.num_sessions - self.sessions_used
        return 0

    def __str__(self):
        return self.user.username



