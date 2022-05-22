from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.conf import settings
import os


class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, username, password, **other_fields):
        if not email:
            raise ValueError('You must provide an Email Address')
        if not username:
            raise ValueError("User must have an username")
        if not password:
            raise ValueError("User must have a password")
        email = self.normalize_email(email)
        user = self.model(
                    email=email, username=username,
                    **other_fields
                    )
        user.set_password(password)
        user.save()
        return user


    def create_superuser(self, email, username, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_superuser', True)


        if not other_fields.get('is_active'):
            raise ValueError("SuperUser must have assigned is_active=True")
        if not other_fields.get('is_staff'):
            raise ValueError("SuperUser must have assigned is_staff=True")
        if not other_fields.get('is_superuser'):
            raise ValueError("SuperUser must have assigned is_superuser=True")
        
        user = self.create_user(email, username, password, **other_fields)
        return user



class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=255)
    email = models.EmailField(unique=True)

    is_staff = models.BooleanField(default=False) 
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    def __str__(self) -> str:
        return str(self.username)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
