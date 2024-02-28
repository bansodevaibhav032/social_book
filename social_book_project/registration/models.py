# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import date

class CustomUser(AbstractUser):    
    username = models.CharField(max_length=30, unique=True, default='default_username')
    email = models.EmailField(unique=True)
    public_visibility = models.BooleanField(default=False)
    birth_year = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def age(self):
        if self.birth_year:
            current_year = date.today().year
            return current_year - self.birth_year
        return None
    age.admin_order_field = 'birth_year'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name', 'last_name']

    def save(self, *args, **kwargs):
        # Calculate age based on the birth year
        if self.birth_year:
            current_year = timezone.now().year
            self.age = current_year - self.birth_year
        super().save(*args, **kwargs)
