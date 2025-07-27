from rest_framework import permissions
from .models import Conversation


class IsParticipantOfConversation(permissions.BasePermission):
    message = "Access Denied!"

    def has_permission(self, request, view):
        conversation_id = (
            request.GET["conversation_id"] or request.POST["conversation_id"]
        )
        convo = Conversation.objects.get(pk=conversation_id)
        user = request.user
        return (
            user.is_authenticated
            and convo.participants.filter(user_id=user).exists()
        )

    def has_object_permission(self, request, view, obj):

        if request.method in ["PUT", "PATCH", "DELETE"]:
            # Instance must have an attribute named `owner`.
            return obj.participants.filter(request.user).exists()
