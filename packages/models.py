from django.db import models

# Package that a student can purchase


class Package(models.Model):
    package_name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    num_sessions = models.PositiveIntegerField(default=1)

    feature1 = models.CharField(max_length=255, blank=True)
    feature2 = models.CharField(max_length=255, blank=True)
    feature3 = models.CharField(max_length=255, blank=True)
    feature4 = models.CharField(max_length=255, blank=True)
    feature5 = models.CharField(max_length=255, blank=True)

    ideal_for = models.TextField(blank=True)

    def __str__(self):
        return self.name

