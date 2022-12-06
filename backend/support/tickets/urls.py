from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TicketResponseViewSet, TicketViewSet

router_v1 = DefaultRouter()
router_v1.register('tickets', TicketViewSet, basename='tickets')
router_v1.register(
    r'tickets/(?P<ticket_id>\d+)/messages', TicketResponseViewSet,
    basename='messages'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
