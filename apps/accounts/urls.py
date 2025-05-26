from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from apps.accounts.rest_views import PoliceUserObtainPairView

urlpatterns = [
    # Login
    path('token/', PoliceUserObtainPairView.as_view(), name='token_obtain'),
    # Refresh token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
