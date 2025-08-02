from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification

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
