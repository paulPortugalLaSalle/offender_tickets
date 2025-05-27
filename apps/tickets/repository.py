from abc import ABC, abstractmethod
from typing import Optional, List

from .domain import Ticket


class TicketRepository(ABC):
    @abstractmethod
    def get_by_id(self, ticket_id: int) -> Optional[Ticket]:
        pass

    @abstractmethod
    def list_by_offender(self, offender_id: str) -> List[Ticket]:
        pass

    @abstractmethod
    def save(self, ticket: Ticket) -> Ticket:
        pass


# Implementación concreta usando Django ORM
from apps.tickets.models import Ticket as TicketModel
from apps.tickets.domain import Offender, Vehicle, Ticket as DomainTicket
from datetime import datetime


class DjangoORMTicketRepository(TicketRepository):
    def get_by_id(self, ticket_id: int) -> Optional[DomainTicket]:
        try:
            obj = TicketModel.objects.get(id=ticket_id)
            return self._to_domain(obj)
        except TicketModel.DoesNotExist:
            return None

    def list_by_offender(self, offender_id: str) -> List[DomainTicket]:
        queryset = TicketModel.objects.filter(offender__identifier=offender_id)
        return [self._to_domain(obj) for obj in queryset]

    def save(self, ticket: DomainTicket) -> DomainTicket:
        obj, _ = TicketModel.objects.update_or_create(
            id=ticket.id,
            defaults={
                'vehicle': ticket.vehicle.identifier,
                'offender_id': ticket.offender.identifier,
                'amount': ticket.amount,
                'description': ticket.description,
                'created_by': ticket.created_by,
            }
        )
        return self._to_domain(obj)

    def _to_domain(self, obj: TicketModel) -> DomainTicket:
        return DomainTicket(
            id=obj.id,
            vehicle=Vehicle(identifier=obj.vehicle.identifier),
            offender=Offender(identifier=obj.offender.identifier, names=obj.offender.names),
            amount=obj.amount,
            description=obj.description,
            created_at=obj.created_date,
            created_by=obj.created_by.username
        )
