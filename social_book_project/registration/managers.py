# managers.py
from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        # Ensure that the required fields are set
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)

        # Create a new user instance with the required fields
        user = self.model(email=email, **extra_fields)

        # Set the password and save the user
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # Set additional fields for superuser
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Call create_user with the required fields
        return self.create_user(email, password=password, **extra_fields)
