# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import date
from .managers import UserManager
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken


class CustomUser(AbstractUser):   
    username = None
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)
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
                pass
        super().save(*args, **kwargs)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = UserManager()

    def get_token(self):
        refresh = RefreshToken.for_user(self)
        return str(refresh.access_token)

    def __str__(self):
        return f"{self.email} - {self.get_token()}"
    

class UploadedFile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/', help_text="Upload PDF ")
    cover_photo = models.ImageField(upload_to='covers/', null=True, blank=True)
    description = models.TextField(blank=True)
    visibility = models.BooleanField(default=True, help_text="Set visibility")
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    year_published = models.PositiveIntegerField(blank=True, null=True)

    def get_cover_photo_url(self):
        if self.cover_photo:
            return self.cover_photo.url
        return None

    def __str__(self):
        return self.title