from rest_framework import serializers

from apps.accounts.models import OffenderUser
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
            'vehicle',
            'offender',
            'amount',
            'description',
            'date',
            'police_names'
        )

    def get_police_names(self, obj):
        return obj.get_police_names


class TicketCreateSerializer(serializers.ModelSerializer):
    vehicle = serializers.CharField(max_length=16, write_only=True, required=True)
    offender_ident = serializers.CharField(max_length=16, write_only=True, required=True)
    offender_names = serializers.CharField(max_length=64, allow_null=True, required=False)

    class Meta:
        model = Ticket
        fields = (
            'vehicle',
            'offender_ident',
            'offender_names',
            'amount',
            'description',
            'date',
        )

    def get_request_fields(self, validated_data):
        vehicle_plate = validated_data.pop('vehicle')
        offender_ident = validated_data.pop('offender_ident')
        offender_names = validated_data.pop('offender_names', '')

        vehicle_obj, v_created = Vehicle.objects.get_or_create(identifier=vehicle_plate)
        offender_obj, o_created = OffenderUser.objects.get_or_create(
            identifier=offender_ident,
            defaults={'names': offender_names}
        )
        return vehicle_obj, offender_obj

    def create(self, validated_data):
        vehicle, offender = self.get_request_fields(validated_data)
        ticket = Ticket.objects.create(
            vehicle=vehicle,
            offender=offender,
            created_by=self.context['request'].user,
            **validated_data
        )
        return ticket

    def update(self, instance, validated_data):
        offender_names = validated_data.get('offender_names')
        vehicle, offender = self.get_request_fields(validated_data)
        offender.names = offender_names
        offender.save()
        instance.vehicle = vehicle
        instance.offender = offender
        instance.created_by = self.context['request'].user
        instance.amount = validated_data.get('amount')
        instance.description = validated_data.get('description')
        instance.save()
        return instance
