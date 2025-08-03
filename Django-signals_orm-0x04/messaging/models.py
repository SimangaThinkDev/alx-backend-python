from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .managers import UnreadMessagesManager # Import the custom manager

class Message(models.Model):
    """
    A model to store messages between users.
    """
    # Assign the custom manager to the objects attribute
    objects = UnreadMessagesManager()

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        verbose_name='Sender'
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages',
        verbose_name='Receiver'
    )
    content = models.TextField(
        verbose_name='Content'
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Timestamp'
    )
    edited = models.BooleanField(
        default=False,
        verbose_name='Edited'
    )
    unread = models.BooleanField(
        default=True,
        verbose_name='Unread'
    )

    class Meta:
        """
        Meta options for the Message model.
        """
        ordering = ['-timestamp']  # Orders messages from newest to oldest
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def __str__(self):
        """
        Returns a string representation of the message.
        """
        return f'From {self.sender.username} to {self.receiver.username} at {self.timestamp}'

class Notification(models.Model):
    """
    A model to store notifications for users.
    Each notification is linked to a user and can be linked to a specific message.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='User'
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='Related Message',
        null=True,  # Notification might not always be related to a message
        blank=True
    )
    content = models.CharField(
        max_length=255,
        verbose_name='Content'
    )
    is_read = models.BooleanField(
        default=False,
        verbose_name='Is Read'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created At'
    )

    class Meta:
        """
        Meta options for the Notification model.
        """
        ordering = ['-created_at']  # Orders notifications from newest to oldest
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'

    def __str__(self):
        """
        Returns a string representation of the notification.
        """
        return f'Notification for {self.user.username}: {self.content[:30]}...'


class MessageHistory(models.Model):
    """
    A model to store the history of edited messages.
    """
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='history',
        verbose_name='Original Message'
    )
    content = models.TextField(
        verbose_name='Old Content'
    )
    edited_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Edited At'
    )

    class Meta:
        """
        Meta options for the MessageHistory model.
        """
        ordering = ['-edited_at']
        verbose_name = 'Message History'
        verbose_name_plural = 'Message Histories'

    def __str__(self):
        """
        Returns a string representation of the message history.
        """
        return f'History for message {self.message.id} edited at {self.edited_at}'
