from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from .models import Thread, Message

User = get_user_model()

class CreateThreadSerializer(serializers.ModelSerializer):
    participant_uuid = serializers.UUIDField(write_only=True)

    class Meta:
        model = Thread
        exclude = ('participants',)

    def validate_participant_uuid(self, value):
        try:
            participant = User.objects.get(pk=value)
        except User.DoesNotExist:
            raise ValidationError("User does not exist.")

        request = self.context.get('request')
        user = request.user
        if user.pk == participant.pk:
            raise ValidationError("You cannot create a thread with yourself.")

        return value

class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = '__all__'


class CreateMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        exclude = ('sender', 'created', 'is_read')

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'