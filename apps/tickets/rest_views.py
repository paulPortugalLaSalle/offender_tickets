import logging

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.tickets.models import Ticket
from apps.tickets.penalty_calculator import SimplePenaltyCalculator
from apps.tickets.repository import DjangoORMTicketRepository
from apps.tickets.serializers import (
    TicketSerializer,
    TicketCreateSerializer,
    TicketUpdateSerializer,
)
from core.constants import (
    REQUEST_TYPE_GET,
    REQUEST_TYPE_POST,
    REQUEST_TYPE_PUT,
    REQUEST_TYPE_DELETE,
)

from .services import TicketService


ticket_service = TicketService(
    repo=DjangoORMTicketRepository(),
    calculator=SimplePenaltyCalculator()
)
logger = logging.getLogger('tickets')


"""
View Rest encargado de ver elas infracciones por policia
"""
@api_view([REQUEST_TYPE_GET])
@permission_classes([IsAuthenticated])
def list_tickets(request,):
    data_response, status_code = ticket_service.filter_tickets(user=request.user)
    return Response(data_response, status=status_code)


"""
View Rest encargado de hacer las consultas a las infracciones
"""
@api_view([REQUEST_TYPE_GET])
def list_ticket_filter(request):
    if not request.query_params:
        return Response({'Error': 'Es necesario establecer filtros'}, status=status.HTTP_204_NO_CONTENT)
    data_response, status_code = ticket_service.filter_tickets(
        vehicle=request.query_params.get('vehicle_id'),
        offender=request.query_params.get('offender_id'),
    )
    return Response(data_response, status=status_code)


"""
View Rest encargado de crear una infraccion.
"""
@api_view([REQUEST_TYPE_POST])
@permission_classes([IsAuthenticated])
def create_ticket(request):
    serializer = TicketCreateSerializer(data=request.data)
    data_response = ticket_service.create_ticket(serializer, user=request.user)
    return Response(data_response, status=status.HTTP_201_CREATED)


"""
View Rest encargado de ver el detalle, actualizar o borrar una infraccion.
"""
@api_view([REQUEST_TYPE_GET, REQUEST_TYPE_PUT, REQUEST_TYPE_DELETE])
@permission_classes([IsAuthenticated])
def get_ticket(request, pk=None):
    ticket = ticket_service.get_ticket(pk=pk)
    if not ticket:
        logger.error(f'Error en la conulta de la infraccion')
        return Response(
            {'error': 'No exiten estos datos de infraccion'},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == REQUEST_TYPE_GET:
        serializer = TicketSerializer(ticket)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == REQUEST_TYPE_PUT:
        serializer = TicketUpdateSerializer(data=request.data)
        data_response, status_code = ticket_service.update_ticket(
            pk,
            serializer,
            user=request.user
        )
        return Response(data_response, status=status_code)

    elif request.method == REQUEST_TYPE_DELETE:
        data_response, status_code = ticket_service.delete_ticket(
            ticket.id,
            user=request.user
        )
        return Response(data_response, status=status_code)
    return None
