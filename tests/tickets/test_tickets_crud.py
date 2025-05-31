from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import PoliceUser, OffenderUser
from apps.tickets.models import Ticket
from apps.vehicles.models import Vehicle
from core.constants import TICKET_TYPE_LEVE


class ListTickets(APITestCase):
    def setUp(self):
        self.password = "plop123PLOP"
        self.user = PoliceUser.objects.create_user(
            email="police1@gmail.com",
            username="police1",
            first_name="paul",
            last_name="portugal herencia",
            password=self.password,
        )
        self.user.set_password(self.password)
        self.user.save()
        response = self.client.post(reverse('token_obtain'), {
            'email': 'police1@gmail.com',
            'password': self.password,
        }, format='json')
        self.token = "Bearer " + response.data['access']

        self.add_ticket_url = reverse('create-ticket')

        self.ticket_data = {
            "vehicle": "placa1",
            "offender_ident": "70185023",
            "offender_names": "paul portugal ofender",
            "ticket_type": TICKET_TYPE_LEVE,
            "amount": 10.45,
            "description": "Infracción leve"
        }

        offender, created = OffenderUser.objects.get_or_create(
            identifier="offender1",
            names="paul portugal ofender",
        )
        vehicle, created = Vehicle.objects.get_or_create(
            identifier="vehiculo_por_actualizar",
        )

        self.ticket = Ticket.objects.create(
            vehicle=vehicle,
            created_by=self.user,
            offender=offender,
            description="ticket por actualizar",
            amount=100.22
        )
        self.ticket.save()

    def test_success_create_minor_ticket(self):
        response = self.client.post(
            self.add_ticket_url,
            self.ticket_data,
            format='json',
            headers={'Authorization': self.token}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['vehicle']['identifier'], 'placa1')
        self.assertEqual(response.data['offender']['identifier'], '70185023')
        self.assertEqual(response.data['amount'], 150)
        self.assertEqual(response.data['police_names'], 'paul portugal herencia')
        self.assertIsNotNone(response.data['created_date'])

    def test_get_ticket_detail(self):
        response = self.client.get(
            reverse('get-ticket', kwargs={'pk': self.ticket.pk}),
            headers={'Authorization': self.token}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['vehicle']['identifier'], 'vehiculo_por_actualizar')
        self.assertEqual(response.data['offender']['identifier'], 'offender1')
        self.assertEqual(response.data['amount'], 100.22)
        self.assertEqual(response.data['police_names'], 'paul portugal herencia')
        self.assertIsNotNone(response.data['created_date'])

    def test_success_update_ticket(self):
        response = self.client.put(
            reverse('get-ticket', kwargs={'pk': self.ticket.pk}),
            self.ticket_data,
            format='json',
            headers={'Authorization': self.token}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['vehicle']['identifier'], 'placa1')
        self.assertEqual(response.data['offender']['identifier'], '70185023')
        self.assertEqual(response.data['amount'], 10.45)
        self.assertEqual(response.data['police_names'], 'paul portugal herencia')
        self.assertIsNotNone(response.data['created_date'])

    def test_success_delete_ticket(self):
        response = self.client.delete(
            reverse('get-ticket', kwargs={'pk': self.ticket.pk}),
            headers={'Authorization': self.token}
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
