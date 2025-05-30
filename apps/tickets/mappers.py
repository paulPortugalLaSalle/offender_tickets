from datetime import datetime

from apps.accounts.domain import Offender
from apps.tickets.domain import Ticket
from apps.vehicles.domain import Vehicle


def make_ticket_from_validated(validated_data, user, amount, ticket_id=None) -> Ticket:
    return Ticket(
        id=ticket_id,
        ticket_type=validated_data['ticket_type'],
        vehicle=Vehicle(identifier=validated_data['vehicle']),
        offender=Offender(
            identifier=validated_data['offender_ident'],
            names=validated_data['offender_names']
        ),
        amount=amount,
        description=validated_data['description'],
        created_at=datetime.now(),
        created_by=user.id
    )
