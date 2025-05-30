from abc import abstractmethod, ABC

from apps.tickets.models import Ticket
from core.constants import (
    TICKET_TYPE_GRAVE,
    TICKET_TYPE_MEDIA,
    TICKET_TYPE_LEVE,
)


class PenaltyCalculator(ABC):
    @abstractmethod
    def calculate(self, ticket_type: str, past_tickets_count: int) -> float:
        pass


class SimplePenaltyCalculator(PenaltyCalculator):
    def calculate(self, ticket_type: str, past_tickets: int) -> float:
        base = 100
        if ticket_type == TICKET_TYPE_LEVE:
            base += 50
        elif ticket_type == TICKET_TYPE_MEDIA:
            base += 100
        elif ticket_type == TICKET_TYPE_GRAVE:
            base += 150
        if past_tickets > 1:
            base += 50
        return base
