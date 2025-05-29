import logging
from datetime import datetime

from apps.accounts.domain import Offender
from apps.tickets.domain import Ticket
from apps.tickets.penalty_calculator import PenaltyCalculator
from apps.tickets.repository import TicketRepository
from apps.vehicles.domain import Vehicle


logger = logging.getLogger('tickets')


class TicketService:
    def __init__(self, repo: TicketRepository, calculator: PenaltyCalculator):
        self.repo = repo
        self.calculator = calculator

    def create_ticket(self, validated_data, user):
        past_tickets = self.repo.list_by_offender(offender_id=validated_data['offender_ident'])
        amount = self.calculator.calculate(validated_data['ticket_type'], len(past_tickets))
        ticket = Ticket(
            id=None,
            ticket_type=validated_data['ticket_type'],
            vehicle=Vehicle(identifier=validated_data['vehicle']),
            offender=Offender(validated_data['offender_ident'], validated_data['offender_names']),
            amount=amount,
            description=validated_data['description'],
            created_at=datetime.now(),
            created_by=user.id
        )
        logger.info(f'Infrancción creado por usuario {user.username} para vehículo {ticket.vehicle.identifier}')
        return self.repo.save(ticket)

    def filter_tickets(self, offender=None, vehicle=None):
        if offender:
            logger.info(f"Consulta de infracciones para por el infractor {offender}")
            return self.repo.list_by_offender(offender_id=offender)
        if vehicle:
            logger.info(f"Consulta de infracciones para vehículo {Vehicle}")
            return self.repo.list_by_vehicle(vehicle_id=vehicle)
        return []
