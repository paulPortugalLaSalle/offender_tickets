import logging

from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.accounts.models import OffenderUser


logger = logging.getLogger('tickets')


class PoliceUserSerializer(TokenObtainPairSerializer):
    username = 'email'

    def validate(self, attrs):
        credentials = {
            self.username_field: attrs.get(self.username_field),
            'password': attrs.get('password')
        }
        user = authenticate(**credentials)

        if not user:
            raise AuthenticationFailed("No se pudo autenticar con esas credenciales")
        if not user.is_active:
            raise AuthenticationFailed("Usuario inactivo")

        logger.info(f'Ingreso el usuario {user.email} al sistema')
        data = super().validate(attrs)
        return data


class OffenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OffenderUser
        fields = '__all__'
