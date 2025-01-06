from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from datetime import date

class CustomUser(AbstractUser):
    # Removing the username field and using email as the unique identifier
    username = None
    email = models.EmailField(_("email_address"), unique=True)
    
    # Additional fields
    public_visibility = models.BooleanField(default=True)  # Visibility setting
    birth_year = models.PositiveIntegerField(null=True, blank=True)  # Birth year field
    address = models.CharField(max_length=255, null=True, blank=True)  # Address field

    # Dynamically calculate the age based on the birth year
    @property
    def age(self):
        if self.birth_year:
            current_year = date.today().year
            return current_year - self.birth_year
        return None

    # Authentication settings
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # No need for username, as we're using email for authentication

    objects = CustomUserManager()

    def __str__(self):
        return self.email
