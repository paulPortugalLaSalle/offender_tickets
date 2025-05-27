from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Offender:
    identifier: str
    names: str


@dataclass
class Vehicle:
    identifier: str

@dataclass
class Ticket:
    id: Optional[int]
    offender: Offender
    vehicle: Vehicle
    amount: float
    description: str
    created_at: datetime
    created_by: int

    # consulta si el infractor tiene mas de una infraccion
    def is_recurrent(self, past_tickets_count: int) -> bool:
        return past_tickets_count > 1
