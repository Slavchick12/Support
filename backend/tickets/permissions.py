from rest_framework import permissions

from .models import Ticket, TicketResponse


class IsSupportCantPOSTPermission(permissions.BasePermission):
    '''
    Support не может отправлять запрос на создание данных.
    '''
    def has_permission(self, request, view):
        if request.method == 'POST':
            return (
                request.user.is_client or request.user.is_superuser
                or request.user.is_admin
            )
        return True


class IsSupportCantEditPermission(permissions.BasePermission):
    '''
    Support не может отправлять запрос на изменение чужих данных.
    '''
    def has_object_permission(self, request, view, obj):
        if request.method == 'PUT' or request.method == 'PATCH':
            return (
                obj.user == request.user or request.user.is_client
                or request.user.is_superuser or request.user.is_admin
            )
        return True


class IsClientCantAnotherMSGPermission(permissions.BasePermission):
    '''
    Client не может отправлять запрос на создание/обновление/удаление данных,
    если объект не его.
    '''
    def has_object_permission(self, request, view, obj):
        print(self)
        if request.method not in permissions.SAFE_METHODS:
            return (
                obj.user == request.user or request.user.is_superuser
                or request.user.is_support or request.user.is_admin
            )
        return True


class IsClientCantRequestPermission(permissions.BasePermission):
    '''
    Client не может отправлять запросы на создание/обновление/удаление данных,
    если объект ticket не его.
    '''
    def has_permission(self, request, view):
        current_user = request.user
        ticket_id = view.kwargs['ticket_id']
        ticket_author = Ticket.objects.get(id=ticket_id).user
        try:
            msg_id = view.kwargs['pk']
            msg_author = TicketResponse.objects.get(id=msg_id).user
        except KeyError:
            msg_author = current_user
        if request.method not in permissions.SAFE_METHODS:
            return (
                (ticket_author == current_user and msg_author == current_user)
                or current_user.is_superuser
                or current_user.is_support or current_user.is_admin
            )
        return True
