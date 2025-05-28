import logging

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.tickets.models import Ticket
from apps.tickets.penalty_calculator import SimplePenaltyCalculator
from apps.tickets.repository import DjangoORMTicketRepository
from apps.tickets.serializers import TicketSerializer, TicketCreateSerializer

from .services import TicketService


logger = logging.getLogger('tickets')

"""
View Rest encargado de ver elas infracciones por policia
"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_tickets(request,):
    if request.method == 'GET':
        tickets = Ticket.objects.filter(created_by=request.user)
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

"""
View Rest encargado de hacer las consultas a las infracciones
"""
@api_view(['GET'])
def list_ticket_filter(request):
    if request.query_params.get('vehicle_id'):
        tickets = Ticket.objects.filter(
            vehicle__identifier=request.query_params.get('vehicle_id')
        )
        serializer = TicketSerializer(tickets, many=True)
        logger.info(f"Consulta de infracciones para vehículo {request.query_params.get('vehicle_id')}")
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.query_params.get('offender_id'):
        tickets = Ticket.objects.filter(
            offender__identifier=request.query_params.get('offender_id')
        )
        serializer = TicketSerializer(tickets, many=True)
        logger.info(f"Consulta de infracciones para por el infractor {request.query_params.get('offender_id')}")
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({'Error': 'No puso ningun filtro'}, status=status.HTTP_204_NO_CONTENT)


"""
View Rest encargado de crear una infraccion.
"""
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_ticket(request):
    if request.method == 'POST':
        serializer = TicketCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            ticket_service = TicketService(
                repo=DjangoORMTicketRepository(),
                calculator=SimplePenaltyCalculator()
            )
            ticket = ticket_service.create_ticket(serializer.validated_data, user=request.user)
            logger.info(f'Infrancción creado por usuario {request.user.username} para vehículo {ticket.vehicle.identifier}')
            return Response(
                {
                    'id': ticket.id,
                    'ticket_type': ticket.ticket_type,
                    'vehicle': {"identifier": ticket.vehicle.identifier},
                    'offender': {"identifier": ticket.offender.identifier, "names": ticket.offender.names},
                    'amount': ticket.amount,
                    'description': ticket.description,
                    'created_at': ticket.created_at,
                    'created_by': ticket.created_by,
                },
                status=status.HTTP_201_CREATED
            )
        else:
            logger.error(f'Error al crear infracción: {serializer.errors}')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
View Rest encargado de ver el detalle, actualizar o borrar una infraccion.
"""
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def get_ticket(request, pk=None):
    try: 
        ticket = Ticket.objects.get(id=pk)
    except Ticket.DoesNotExist:
        logger.error(f'Error en la conulta de la infraccion')
        return Response({'error': 'No exiten estos datos de infraccion'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TicketSerializer(ticket, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        if ticket.created_by != request.user:
            return Response(
                {'error': 'No tienes permiso para editar esta infraccion'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = TicketCreateSerializer(ticket, data=request.data, context={'request': request})
        if serializer.is_valid():
            ticket = serializer.save()
            logger.info(
                f'Infrancción con id {ticket.id} ha sido modificado')
            return Response(
                TicketSerializer(ticket, many=False).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if ticket.created_by != request.user:
            return Response(
                {'error': 'No tienes permiso para eliminar esta infraccion'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        ticket.delete()
        logger.info(f'Infrancción con id {ticket.id} ha sido eliminado')
        return Response(status=status.HTTP_204_NO_CONTENT)
