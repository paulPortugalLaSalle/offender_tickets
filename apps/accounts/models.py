from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.password_validation import validate_password
from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.exceptions import ValidationError


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        try:
            validate_password(password, user)
        except ValidationError as e:
            raise ValueError(f'Contraseña invalida: {e.messages}')
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class PoliceUser(AbstractUser):
    email = models.EmailField(unique=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if self.is_superuser:
            return super().save(*args, **kwargs)
        if self.pk is None or not PoliceUser.objects.filter(pk=self.pk).exists():
            self.set_password(self.password)
        super(PoliceUser, self).save(*args, **kwargs)


class OffenderUser(models.Model):
    identifier = models.CharField(max_length=16, unique=True)
    names = models.CharField(max_length=64, blank=True)

    class Meta:
        verbose_name = 'Infractor'

    def __str__(self):
        return f'{self.names} - {self.identifier}'
