from django.db import models
from django.contrib.auth.models import BaseUserManager


class UserAccountManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError("You have not provided an email address")
        email = self.normalize_email(email).lower()

        user = self.model(
            email=email, first_name=first_name, last_name=last_name, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_admin(self, email, first_name, last_name, password=None, **extra_fields):
        user = self.create_user( 
            email=email, first_name=first_name, last_name=last_name, password=password, **extra_fields
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        user = self.create_user(
            email=email, first_name=first_name, last_name=last_name, password=password, **extra_fields
        )

        user.is_staff = True
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user
