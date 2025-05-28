from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from apps.accounts.domain import Offender
from apps.vehicles.domain import Vehicle


@dataclass
class Ticket:
    id: Optional[int]
    offender: Offender
    vehicle: Vehicle
    amount: float
    ticket_type: str
    description: str
    created_at: datetime
    created_by: int

    # consulta si el infractor tiene mas de una infraccion
    def is_recurrent(self, past_tickets_count: int) -> bool:
        return past_tickets_count > 1
