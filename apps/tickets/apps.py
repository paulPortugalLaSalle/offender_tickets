from django.apps import AppConfig


ticket_service = None


class TicketsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.tickets'

    def ready(self):
        from apps.tickets.services import TicketService
        from apps.tickets.repository import DjangoORMTicketRepository
        from apps.tickets.penalty_calculator import SimplePenaltyCalculator

        global ticket_service
        ticket_service = TicketService(
            repo=DjangoORMTicketRepository,
            calculator=SimplePenaltyCalculator
        )
