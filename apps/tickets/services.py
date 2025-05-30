import logging
from datetime import datetime

from apps.accounts.domain import Offender
from apps.tickets.domain import Ticket
from apps.tickets.mappers import make_ticket_from_validated
from apps.tickets.penalty_calculator import PenaltyCalculator
from apps.tickets.repository import TicketRepository
from apps.tickets.serializers import TicketSerializer, TicketAfterCreateSerializer
from apps.vehicles.domain import Vehicle


logger = logging.getLogger('tickets')


class TicketService:
    def __init__(self, repo: TicketRepository, calculator: PenaltyCalculator):
        self.repo = repo
        self.calculator = calculator

    def create_ticket(self, serializer, user):
        if serializer.is_valid():
            past_tickets = self.repo.list_by_offender(
                offender_id=serializer.validated_data['offender_ident']
            )
            amount = self.calculator.calculate(
                serializer.validated_data['ticket_type'],
                len(past_tickets)
            )
            ticket = self.repo.save(
                make_ticket_from_validated(
                    validated_data=serializer.validated_data,
                    user=user,
                    amount=amount
                )
            )
            logger.info(f'Infrancción creado por usuario {user.username} para vehículo {ticket.vehicle.identifier}')
            return TicketAfterCreateSerializer(ticket, many=False).data
        else:
            return serializer.errors

    def update_ticket(self, ticket_id, serializer, user):
        ticket = self.repo.get_by_id(ticket_id)
        if not ticket:
            return {'error': 'Ticket no encontrado'}, 404

        if ticket.created_by != user.id:
            return {'error': 'No tienes permiso para editar esta infracción'}, 401

        if not serializer.is_valid():
            return serializer.errors, 400

        ticket = self.repo.save(
            make_ticket_from_validated(
                validated_data=serializer.validated_data,
                user=user,
                amount=serializer.validated_data['amount'],
                ticket_id=ticket_id
            )
        )
        logger.info(f'Infrancción con id {ticket.id} ha sido modificado')
        return TicketAfterCreateSerializer(ticket, many=False).data, 201

    def filter_tickets(self, offender=None, vehicle=None, user=None):
        def serialize_or_404(tickets, context_info):
            if not tickets:
                return [], 204
            logger.info(context_info)
            return TicketSerializer(tickets, many=True).data, 200

        if offender:
            tickets = self.repo.list_by_offender(offender_id=offender)
            return serialize_or_404(tickets, f"Consulta de infracciones por el infractor {offender}")

        if vehicle:
            tickets = self.repo.list_by_vehicle(vehicle)
            return serialize_or_404(tickets, f"Consulta de infracciones para vehículo {vehicle}")

        if user:
            tickets = self.repo.list_by_user(user.id)
            return serialize_or_404(tickets, f"Consulta de infracciones del policía con correo {user.email}")

        return [], 204

    def get_ticket(self,pk):
        return self.repo.get_by_id(pk)

    def delete_ticket(self, ticket_id, user=None):
        ticket = self.repo.get_by_id(ticket_id)
        if not ticket:
            return {'error': 'Ticket no encontrado'}, 404

        if ticket.created_by != user.id:
            return {'error': 'No tienes permiso para eliminar esta infracción'}, 401
        logging.info(f'Infrancción con id {ticket_id} ha sido eliminado')
        self.repo.delete(ticket_id)
        return {'eliminado': True}, 204
