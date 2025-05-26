import datetime

from django.db import models

from core.models import BaseModel
from apps.accounts.models import OffenderUser
from apps.vehicles.models import Vehicle


class Ticket(BaseModel):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    offender = models.ForeignKey(
        OffenderUser,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    amount = models.FloatField(verbose_name='multa')
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name="descripcion"
    )
    date = models.DateField(default=datetime.date.today, verbose_name="fecha")

    def __str__(self):
        return f"placa: {self.vehicle} - infractor: {self.offender.names} - multa: {self.amount}"
