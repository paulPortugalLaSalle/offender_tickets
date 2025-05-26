from django.urls import path

from apps.tickets.rest_views import (
    list_tickets,
    create_ticket,
    get_ticket,
    list_ticket_filter,
)

urlpatterns = [
    path('list/', list_tickets, name='tickets-list'),
    path('filter/', list_ticket_filter, name='tickets-list-by-vehicle'),
    path('create/', create_ticket, name='create-ticket'),
    path('ticket/<int:pk>/', get_ticket, name='get-ticket'),
]
