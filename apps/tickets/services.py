from datetime import datetime

from apps.tickets.domain import Ticket, Vehicle, Offender
from apps.tickets.penalty_calculator import PenaltyCalculator
from apps.tickets.repository import TicketRepository


class TicketService:
    def __init__(self, repo: TicketRepository, calculator: PenaltyCalculator):
        self.repo = repo
        self.calculator = calculator

    def create_ticket(self, vehicle: str, offender_ident: str, offender_names: str, description: str, created_by: int):
        past_tickets = self.repo.list_by_offender(offender_ident)
        amount = self.calculator.calculate(len(past_tickets))

        ticket = Ticket(
            id=None,
            vehicle=Vehicle(vehicle),
            offender=Offender(offender_ident, offender_names),
            amount=amount,
            description=description,
            created_at=datetime.now(),
            created_by=created_by
        )
        return self.repo.save(ticket)
