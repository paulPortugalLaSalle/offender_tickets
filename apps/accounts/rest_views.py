from rest_framework_simplejwt.views import TokenObtainPairView

from apps.accounts.serializers import PoliceUserSerializer


class PoliceUserObtainPairView(TokenObtainPairView):
    serializer_class = PoliceUserSerializer
