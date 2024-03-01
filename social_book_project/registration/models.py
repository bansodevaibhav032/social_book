# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import date
from .managers import UserManager
from django.conf import settings
from django.contrib.auth import get_user_model
class CustomUser(AbstractUser):   
    username = models.CharField(max_length=30, unique=True, default='john')
    email = models.EmailField(unique=True)
    public_visibility = models.BooleanField(default=False)
    address = models.CharField(max_length=255, blank=True, null=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    birth_year = models.PositiveIntegerField(null=True, blank=True)
  

    def save(self, *args, **kwargs):
        current_year = 2024  
        if self.birth_year:
            try:
                self.birth_year = int(self.birth_year)
                self.age = current_year - self.birth_year
            except ValueError:
                # Handle the case where birth_year is not a valid integer
                pass
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = UserManager()

class UploadedFile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/', help_text="Upload PDF or JPEG files only.")
    description = models.TextField(blank=True)
    visibility = models.BooleanField(default=True, help_text="Set visibility")
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    year_published = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.title