from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
from django.contrib.auth.models import User

# My Signals here

@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance, created, **kwargs):
    """
    Signal handler to create a notification when a new Message is saved.
    This function is triggered by the post_save signal of the Message model.
    The 'created' flag ensures the logic only runs for new instances, not updates.
    """
    if created:
        # Create a new Notification object for the receiver of the message.
        # This links the notification to the receiving user and the specific message.
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            content=f"You have a new message from {instance.sender.username}!"
        )

        # For demonstration, we'll print a confirmation message to the console.
        print(f"New message from {instance.sender.username} to {instance.receiver.username}. A notification has been created.")

@receiver(pre_save, sender=Message)
def log_message_history(sender, instance, **kwargs):
    """
    Signal handler to log the old content of a Message before it is updated.
    This function is triggered by the pre_save signal of the Message model.
    It checks if the instance already has a primary key, indicating it's an update.
    """
    if instance.pk:
        try:
            # Get the original message from the database before the update
            old_message = Message.objects.get(pk=instance.pk)
            # Create a history entry if the content has changed
            if old_message.content != instance.content:
                MessageHistory.objects.create(
                    message=old_message,
                    content=old_message.content
                )
                # Set the edited flag on the message
                instance.edited = True
                print(f"Message {instance.pk} content changed. Old content logged to history.")
        except Message.DoesNotExist:
            # This should not happen in normal circumstances but is good practice to handle
            pass


@receiver( post_delete, sender=User )
def clean_up_after_user( sender, instance, **kwargs ):
    """
    If we look back at the database schema we have
    It seems this is already dealt with, Thanks
    """
    
    # Delete messages sent by the user
    Message.objects.filter(sender=instance).delete()
    
    # Delete messages received by the user
    Message.objects.filter(receiver=instance).delete()
    
    # Delete notifications for the user
    Notification.objects.filter(user=instance).delete()
    
    # Delete message history related to the user's messages
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()
    print(f"User {instance.username} has been deleted. Related data cleaned up.")
    pass