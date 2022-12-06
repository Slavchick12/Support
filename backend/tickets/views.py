from rest_framework import viewsets

from .models import Ticket, TicketResponse
from .permissions import (IsClientCantAnotherMSGPermission,
                          IsClientCantRequestPermission,
                          IsSupportCantEditPermission,
                          IsSupportCantPOSTPermission)
from .serializers import (TicketClientAndAdminSerializer,
                          TicketResponseClientAndAdminSerializer,
                          TicketResponseSupportSerializer,
                          TicketSupportSerializer)


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    permission_classes = (
        IsSupportCantPOSTPermission, IsClientCantAnotherMSGPermission
    )
    ordering_fields = ('-date',)

    def get_serializer_class(self):
        if self.request.user.is_support:
            return TicketSupportSerializer
        return TicketClientAndAdminSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TicketResponseViewSet(viewsets.ModelViewSet):
    queryset = TicketResponse.objects.all()
    permission_classes = (
        IsSupportCantEditPermission, IsClientCantRequestPermission
    )

    def get_serializer_class(self):
        if self.request.user.is_support:
            return TicketResponseSupportSerializer
        return TicketResponseClientAndAdminSerializer

    def perform_create(self, serializer):
        ticket_id = self.kwargs['ticket_id']
        serializer.save(user=self.request.user, ticket_id=ticket_id)
