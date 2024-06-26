from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import LimitOffsetPagination
from django.contrib.auth import get_user_model
from django.db.models import Q

from .models import Thread, Message
from .serializers import CreateThreadSerializer, ThreadSerializer, MessageSerializer, CreateMessageSerializer

# Create your views here.
User = get_user_model()

class CreateThreadView(generics.CreateAPIView):
    queryset = Thread.objects.all()
    serializer_class = CreateThreadSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        participant_uuid = serializer.validated_data.get('participant_uuid')
        user = request.user
        participant = User.objects.get(pk=participant_uuid)


        # Checs if a thread already exists between the curent user and the participant
        thread = Thread.objects.filter(participants=user).filter(participants=participant)
        if thread.exists():
            serializer = CreateThreadSerializer(thread.first())
            return Response(serializer.data, status=status.HTTP_200_OK)

        # create a new one and add participants If thread doesn't exist
        thread = Thread.objects.create()
        thread.participants.add(user, participant)
        serializer = CreateThreadSerializer(thread)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
class DeleteThreadView(generics.DestroyAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        user = request.user
        if user not in instance.participants.all():
            # Checks if the current user is not a participant of the thread
            raise PermissionDenied("You do not have permission to delete this thread.")
        
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class ThreadListView(generics.ListAPIView):
    serializer_class = ThreadSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        user = self.request.user
        return Thread.objects.filter(participants=user)
    

class CreateMessageView(generics.CreateAPIView):
    serializer_class = CreateMessageSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        thread_id = self.kwargs.get('thread_id')
        queryset = Message.objects.filter(thread_id=thread_id).order_by('created')
        user = self.request.user

        for message in queryset:
            # Marks unread messages as read if they were send by other users
            if not message.is_read and message.sender != user:
                message.is_read = True
                message.save()
        
        return queryset
    

class UnreadMessageCountView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        # Retrieves threads in which the user participates
        threads = Thread.objects.filter(participants=user)

        # Counts number of unread mesages in the threads
        unread_count = Message.objects.filter(thread__in=threads, is_read=False).count()
        return Response({'unread_count': unread_count}, status=status.HTTP_200_OK)
    