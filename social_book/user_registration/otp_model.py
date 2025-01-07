from django.db import models
from django.conf import settings  # Import settings to reference the custom user model
from django.utils import timezone
import random
import string

class OTP(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use settings.AUTH_USER_MODEL instead of User
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"OTP for {self.user.email}"

    def is_expired(self):
        return timezone.now() > self.expires_at

    @staticmethod
    def generate_otp():
        return ''.join(random.choices(string.digits, k=6))  # Generate a 6-digit OTP
