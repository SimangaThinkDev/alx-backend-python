from django.db import models

class UnreadMessagesManager(models.Manager):
    """
    Custom manager for the Message model to easily filter unread messages.
    """
    def unread_for_user(self, user):
        """
        Returns a QuerySet of unread messages for a given user.
        """
        return self.filter(receiver=user, read=False)