import uuid

from django.db import models

from core.models import BaseModel


class Vehicle(BaseModel):
    identifier = models.CharField(unique=True, verbose_name="Placa")

    def __str__(self):
        return self.identifier
