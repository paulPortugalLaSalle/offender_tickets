from abc import ABC, abstractmethod
from typing import Optional, List



# Implementación concreta usando Django ORM
from apps.tickets.models import Ticket as TicketModel
from apps.vehicles.models import Vehicle as VehicleModel
from apps.accounts.models import PoliceUser, OffenderUser
from .domain import (
    Offender,
    Vehicle,
    Ticket as DomainTicket
)


class TicketRepository(ABC):
    @abstractmethod
    def get_by_id(self, ticket_id: int) -> Optional[DomainTicket]:
        pass

    @abstractmethod
    def list_by_offender(self, offender_id: str) -> List[DomainTicket]:
        pass

    @abstractmethod
    def list_by_vehicle(self, vehicle_id: str) -> List[DomainTicket]:
        pass

    @abstractmethod
    def list_by_user(self, user: int) -> List[DomainTicket]:
        pass

    @abstractmethod
    def delete(self, ticked_id: int) -> None:
        pass

    @abstractmethod
    def save(self, ticket: DomainTicket) -> DomainTicket:
        pass


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

    def list_by_vehicle(self, vehicle_id: str) -> List[DomainTicket]:
        queryset = TicketModel.objects.filter(vehicle__identifier=vehicle_id)
        return [self._to_domain(obj) for obj in queryset]

    def list_by_user(self, user: int) -> List[DomainTicket]:
        queryset = TicketModel.objects.filter(created_by_id=user)
        return [self._to_domain(obj) for obj in queryset]

    def save(self, ticket: DomainTicket) -> DomainTicket:
        vehicle, _ = VehicleModel.objects.update_or_create(identifier=ticket.vehicle.identifier)
        offender, _ = OffenderUser.objects.update_or_create(
            identifier=ticket.offender.identifier,
            defaults={'names': ticket.offender.names}
        )
        police = PoliceUser.objects.get(id=ticket.created_by)
        obj, _ = TicketModel.objects.update_or_create(
            id=ticket.id,
            defaults={
                'vehicle': vehicle,
                'offender': offender,
                'amount': ticket.amount,
                'ticket_type': ticket.ticket_type,
                'description': ticket.description,
                'created_by': police
            }
        )
        return self._to_domain(obj)


    def delete(self, ticked_id: int) -> None:
        try:
            obj = TicketModel.objects.get(id=ticked_id)
            obj.delete()
        except TicketModel.DoesNotExist:
            pass


    def _to_domain(self, obj: TicketModel) -> DomainTicket:
        return DomainTicket(
            id=obj.id,
            ticket_type=obj.ticket_type,
            vehicle=Vehicle(identifier=obj.vehicle.identifier),
            offender=Offender(identifier=obj.offender.identifier, names=obj.offender.names),
            amount=obj.amount,
            description=obj.description,
            created_date=obj.created_date,
            created_by=obj.created_by.id,
        )
