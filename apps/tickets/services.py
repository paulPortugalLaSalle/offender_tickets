from datetime import datetime

from apps.accounts.domain import Offender
from apps.tickets.domain import Ticket
from apps.tickets.penalty_calculator import PenaltyCalculator
from apps.tickets.repository import TicketRepository
from apps.vehicles.domain import Vehicle


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
        return self.repo.save(ticket)
