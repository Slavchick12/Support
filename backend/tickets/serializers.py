from rest_framework import serializers

from .models import Ticket, TicketResponse
from .support_functions import joint_validate
from .utils import (MESSAGE_RESPONSE_IS_EXISTS, RESPONSE_MESSAGE,
                    SUPPORT_STATUS, TICKET_RESPONSE_IS_EXISTS)


class TicketSupportSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Ticket
        fields = ('user', 'topic', 'descripion', 'file', 'status', 'date')

    def validate(self, data):
        try:
            self.initial_data.pop('status')
            if self.initial_data:
                raise serializers.ValidationError(SUPPORT_STATUS)
        except KeyError:
            raise serializers.ValidationError(SUPPORT_STATUS)
        return data


class TicketClientAndAdminSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Ticket
        fields = ('user', 'topic', 'descripion', 'file', 'status', 'date')


class TicketResponseSupportSerializer(serializers.ModelSerializer):
    ticket = serializers.SlugRelatedField(slug_field='topic', read_only=True)

    class Meta:
        model = TicketResponse
        fields = ('id', 'ticket', 'message', 'text')

    def validate(self, data):
        ticket_id = self.context.get('view').kwargs['ticket_id']
        message = self.initial_data.get('message')
        request = self.context.get('request')
        current_user = request.user
        if message:
            joint_validate(self, message, request, current_user)
        if message is None and TicketResponse.objects.filter(
            message=None, ticket_id=ticket_id
        ).exists():
            raise serializers.ValidationError(TICKET_RESPONSE_IS_EXISTS)
        if (
            request.method == 'POST'
            and TicketResponse.objects.filter(
                message=message, ticket_id=ticket_id
            ).exists()
        ):
            raise serializers.ValidationError(MESSAGE_RESPONSE_IS_EXISTS)
        return data


class TicketResponseClientAndAdminSerializer(serializers.ModelSerializer):
    ticket = serializers.SlugRelatedField(slug_field='topic', read_only=True)

    class Meta:
        model = TicketResponse
        fields = ('id', 'ticket', 'message', 'text')

    def validate(self, data):
        msg_key = 'message'
        message = self.initial_data.get(msg_key)
        request = self.context.get('request')
        current_user = request.user
        if message:
            joint_validate(self, message, request, current_user)
        if message is None and not current_user.is_admin:
            raise serializers.ValidationError({msg_key: RESPONSE_MESSAGE})  # Можно только отвечать на сообщения
        if (
            request.method == 'POST'
            and TicketResponse.objects.filter(message=message).exists()
        ):
            raise serializers.ValidationError(MESSAGE_RESPONSE_IS_EXISTS)
        return data
