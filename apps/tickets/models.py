import datetime

from django.db import models

from core.constants import (
    TICKET_TYPE_LEVE,
    TICKET_TYPE_MEDIA,
    TICKET_TYPE_GRAVE,
)
from core.models import BaseModel
from apps.accounts.models import OffenderUser
from apps.vehicles.models import Vehicle


class Ticket(BaseModel):

    TICKET_TYPE = (
        (TICKET_TYPE_LEVE, "leve"),
        (TICKET_TYPE_MEDIA, "media"),
        (TICKET_TYPE_GRAVE, "grave"),
    )

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
    ticket_type = models.CharField(
        max_length=8,
        verbose_name="tipo de ticket",
        choices=TICKET_TYPE,
        default=TICKET_TYPE_LEVE
    )

    def __str__(self):
        return f"placa: {self.vehicle} - infractor: {self.offender.names} - multa: {self.amount}"
