from django.shortcuts import render

# Create your views here.
# messaging_app/chats/views.py
# messaging_app/chats/views.py

from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__email', 'participants__first_name']

    def create(self, request, *args, **kwargs):
        participant_ids = request.data.get("participants")
        if not participant_ids or not isinstance(participant_ids, list):
            return Response({"error": "Participants must be a list of user IDs."},
                            status=status.HTTP_400_BAD_REQUEST)

        participants = User.objects.filter(user_id__in=participant_ids)
        if participants.count() != len(participant_ids):
            return Response({"error": "One or more users not found."},
                            status=status.HTTP_404_NOT_FOUND)

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['sent_at']
    ordering = ['sent_at']

    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get("conversation_id")
        message_body = request.data.get("message_body")

        if not conversation_id or not message_body:
            return Response({"error": "conversation_id and message_body are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)

        if request.user not in conversation.participants.all():
            return Response({"error": "You are not a participant of this conversation."},
                            status=status.HTTP_403_FORBIDDEN)

        message = Message.objects.create(
            sender=request.user,
            conversation=conversation,
            message_body=message_body
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
