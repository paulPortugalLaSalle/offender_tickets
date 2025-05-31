import unittest
from datetime import datetime
from unittest.mock import MagicMock, Mock, patch

from apps.accounts.domain import Offender
from apps.tickets.domain import Ticket
from apps.tickets.penalty_calculator import SimplePenaltyCalculator
from apps.tickets.services import TicketService
from apps.vehicles.domain import Vehicle
from core.constants import TICKET_TYPE_LEVE


class TicketServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock()
        self.calculator = SimplePenaltyCalculator()
        self.service = TicketService(repo=self.mock_repo, calculator=self.calculator)
        self.mock_user = Mock(id=1, username="police_user")
        self.VEHICLE_IDENTIFIER = "ABC123"
        self.OFFENDER_IDENTIFIER = "12345678"

    def test_create_ticket_successfully(self):
        input_data = {
            'ticket_type': TICKET_TYPE_LEVE,
            'vehicle': self.VEHICLE_IDENTIFIER,
            'offender_ident': self.OFFENDER_IDENTIFIER,
            'offender_names': 'Juan Pérez',
            'description': 'Conducción a exceso de velocidad',
        }

        serializer = MagicMock()
        serializer.is_valid.return_value = True
        serializer.validated_data = input_data

        self.mock_repo.list_by_offender.return_value = []

        domain_ticket = Ticket(
            id=1,
            ticket_type=TICKET_TYPE_LEVE,
            vehicle=Vehicle(identifier='ABC123'),
            offender=Offender(identifier='12345678', names='Juan Pérez'),
            amount=200,
            description='Conducción a exceso de velocidad',
            created_date=datetime.now(),
            created_by=1
        )
        self.mock_repo.save.return_value = domain_ticket

        result = self.service.create_ticket(serializer, self.mock_user)

        # assert
        self.assertIsInstance(result, dict)
        self.assertEqual(result['ticket_type'], TICKET_TYPE_LEVE)
        self.assertEqual(result['amount'], 200)
        self.mock_repo.save.assert_called_once()
        self.mock_repo.list_by_offender.assert_called_once_with(offender_id=self.OFFENDER_IDENTIFIER)

    def test_create_ticket_invalid_serializer(self):
        serializer = MagicMock()
        serializer.is_valid.return_value = False
        serializer.errors = {'ticket_type': ['Este campo es obligatorio.']}

        result = self.service.create_ticket(serializer, self.mock_user)
        self.assertEqual(result, {'ticket_type': ['Este campo es obligatorio.']})

    @patch('apps.tickets.services.TicketSerializer')
    def test_filter_tickets_by_offender_with_results(self, mock_serializer):
        mock_ticket = MagicMock()
        self.mock_repo.list_by_offender.return_value = [mock_ticket]

        mock_serializer.return_value.data = [{'id': 1, 'ticket_type': 'leve'}]

        data, status = self.service.filter_tickets(offender='12345678')

        self.mock_repo.list_by_offender.assert_called_once_with(offender_id='12345678')
        mock_serializer.assert_called_once_with([mock_ticket], many=True)

        self.assertEqual(status, 200)
        self.assertEqual(data, [{'id': 1, 'ticket_type': 'leve'}])

    @patch('apps.tickets.services.TicketSerializer')
    def test_filter_tickets_by_vehicle_with_results(self, mock_serializer):
        mock_ticket = MagicMock()
        self.mock_repo.list_by_vehicle.return_value = [mock_ticket]

        mock_serializer.return_value.data = [{'id': 1, 'ticket_type': 'leve'}]

        data, status = self.service.filter_tickets(vehicle='vehicle1')

        self.mock_repo.list_by_vehicle.assert_called_once_with('vehicle1')
        mock_serializer.assert_called_once_with([mock_ticket], many=True)

        self.assertEqual(status, 200)
        self.assertEqual(data, [{'id': 1, 'ticket_type': 'leve'}])

    def test_filter_tickets_by_offender_without_results(self):
        self.mock_repo.list_by_offender.return_value = []

        data, status = self.service.filter_tickets(offender='12345678')

        self.mock_repo.list_by_offender.assert_called_once_with(offender_id='12345678')
        self.assertEqual(data, [])
        self.assertEqual(status, 204)