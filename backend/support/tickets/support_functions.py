from rest_framework import serializers

from .models import TicketResponse
from .utils import YOUR_MESSAGE


def joint_validate(self, message, request, current_user):
    message_author = TicketResponse.objects.get(id=message).user
    if message_author == current_user and request.method == 'POST':
        raise serializers.ValidationError(YOUR_MESSAGE)
