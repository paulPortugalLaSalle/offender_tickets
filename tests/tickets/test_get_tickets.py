from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import PoliceUser, OffenderUser
from apps.tickets.models import Ticket
from apps.vehicles.models import Vehicle


class ListTickets(APITestCase):
    def setUp(self):
        self.vehicle_one = Vehicle.objects.create(identifier="vehiculo1")
        self.vehicle_two = Vehicle.objects.create(identifier="vehiculo2")
        self.police_one = PoliceUser.objects.create_user(
            email="police1@gmail.com", username="police1", password="plop123PLOP"
        )
        self.police_two = PoliceUser.objects.create_user(
            email="police2@gmail.com", username="police2", password="plop123PLOP"
        )
        self.offender_one = OffenderUser.objects.create(
            identifier="offender_one", names="offender_one_names"
        )
        self.offender_two = OffenderUser.objects.create(
            identifier="offender_two", names="offender_two_names"
        )

        self.ticket_one = Ticket.objects.create(
            vehicle=self.vehicle_one,
            created_by=self.police_one,
            offender=self.offender_one,
            description="ticket One",
            amount=100.11
        )
        self.ticket_two = Ticket.objects.create(
            vehicle=self.vehicle_two,
            created_by=self.police_two,
            offender=self.offender_two,
            description="ticket two",
            amount=100.22
        )
        self.ticket_three = Ticket.objects.create(
            vehicle=self.vehicle_one,
            created_by=self.police_two,
            offender=self.offender_two,
            description="ticket three",
            amount=100.33
        )

        self.list_url = reverse('tickets-list')

    def test_list_tickets_requires_authentication(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_tickets_by_user(self):
        # Policia uno con 1 ticket
        self.client.force_authenticate(user=self.police_one)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['description'], "ticket One")
        # Policia dos con 2 tickets
        self.client.force_authenticate(user=self.police_two)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['description'], "ticket two")
        self.assertEqual(response.data[1]['description'], "ticket three")

    def test_get_ticket_by_vehicle(self):
        filter_by_existing_vehicle = reverse('tickets-list-by-vehicle') + '?vehicle_id=vehiculo1'
        response = self.client.get(filter_by_existing_vehicle)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['vehicle']['identifier'], "vehiculo1")
        self.assertEqual(response.data[1]['vehicle']['identifier'], "vehiculo1")

        filter_by_existing_vehicle = reverse('tickets-list-by-vehicle') + '?vehicle_id=vehiculo2'
        response = self.client.get(filter_by_existing_vehicle)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['vehicle']['identifier'], "vehiculo2")

    def test_get_ticket_by_offender(self):
        filter_by_existing_offender = reverse('tickets-list-by-vehicle') + '?offender_id=offender_one'
        response = self.client.get(filter_by_existing_offender)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['offender']['identifier'], "offender_one")

        filter_by_existing_offender = reverse('tickets-list-by-vehicle') + '?offender_id=offender_two'
        response = self.client.get(filter_by_existing_offender)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['offender']['identifier'], "offender_two")
        self.assertEqual(response.data[1]['offender']['identifier'], "offender_two")

    def test_get_ticket_without_filter(self):
        reverse_without_filters = reverse('tickets-list-by-vehicle')
        response = self.client.get(reverse_without_filters)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
