from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from packages.models import Package


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    package = models.ForeignKey(Package, on_delete=models.SET_NULL, null=True)
    purchased_on = models.DateTimeField(auto_now_add=True)
    expires_on = models.DateTimeField(null=True, blank=True)

    stripe_checkout_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_payment_intent = models.CharField(max_length=255, blank=True, null=True)
    payment_status = models.CharField(max_length=50, default='unconfirmed')

    def sessions_remaining(self):
        if self.package:
            return self.package.num_sessions - self.sessions_used
        return 0

    def __str__(self):
        return f"{self.user.username} – {self.package.name if self.package else 'Unknown Package'}"
