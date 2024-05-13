from django.db import models
from django.utils import timezone
from rest_framework.serializers import ValidationError

import uuid

class Thread(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField('users.CustomUser', related_name='threads')
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.participants.count() > 2:
            raise ValidationError("A thread can't have more than 2 participants.")

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    text = models.TextField()
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)