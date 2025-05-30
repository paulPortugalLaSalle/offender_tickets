from symtable import Class

from rest_framework import serializers

from apps.accounts.models import OffenderUser, PoliceUser
from apps.accounts.serializers import OffenderSerializer
from apps.tickets.models import Ticket
from apps.vehicles.models import Vehicle
from apps.vehicles.serializers import VehicleSerializer


class TicketSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer(read_only=True)
    offender = OffenderSerializer(read_only=True, many=False)
    police_names = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = (
            'id',
            'ticket_type',
            'vehicle',
            'offender',
            'amount',
            'description',
            'date',
            'police_names'
        )

    def get_police_names(self, obj):
        try:
            police_obj = obj.created_by
            if isinstance(police_obj, int):
                obj.created_by = PoliceUser.objects.get(id=police_obj)
            return f"{obj.created_by.first_name} {obj.created_by.last_name}"
        except PoliceUser.DoesNotExist:
            return None


class TicketAfterCreateSerializer(TicketSerializer):
    pass


class TicketAfterUpdateSerializer(TicketSerializer):
    pass


class TicketInputSerializer(serializers.ModelSerializer):
    vehicle = serializers.CharField(max_length=16, write_only=True, required=True)
    offender_ident = serializers.CharField(max_length=16, write_only=True, required=True)
    offender_names = serializers.CharField(max_length=64, allow_null=True, required=False)

    class Meta:
        model = Ticket
        fields = (
            'ticket_type',
            'vehicle',
            'offender_ident',
            'offender_names',
            'description',
            'date',
        )


class TicketCreateSerializer(TicketInputSerializer):
    pass


class TicketUpdateSerializer(TicketInputSerializer):
    class Meta(TicketInputSerializer.Meta):
        fields = TicketInputSerializer.Meta.fields + ('amount',)
