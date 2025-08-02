from django.test import TestCase
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from .models import Message, Notification
from .signals import create_notification_on_message  # Import the signal function

class MessageSignalsTestCase(TestCase):
    """
    Test case to verify the functionality of the post_save signal
    on the Message model, which creates a Notification.
    """
    def setUp(self):
        """
        Set up test users and explicitly connect the signal for the test.
        """
        # Create test users
        self.sender = User.objects.create_user(username='sender_user', password='testpassword')
        self.receiver = User.objects.create_user(username='receiver_user', password='testpassword')
        
        # Explicitly connect the signal handler for this test run.
        # This ensures the signal is active even if the app's ready() method isn't fully
        # invoked in the test environment.
        post_save.connect(create_notification_on_message, sender=Message)

    def tearDown(self):
        """
        Disconnect the signal after each test to prevent side effects.
        """
        post_save.disconnect(create_notification_on_message, sender=Message)

    def test_notification_creation_on_new_message(self):
        """
        Test that a new Notification is created when a Message is saved.
        """
        # Ensure there are no messages or notifications to start.
        self.assertEqual(Message.objects.count(), 0)
        self.assertEqual(Notification.objects.count(), 0)

        # Create a new message instance. This should trigger the signal.
        new_message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Hello there!"
        )

        # After creating the message, a new message should exist.
        self.assertEqual(Message.objects.count(), 1)
        # And a new notification should have been created by the signal.
        self.assertEqual(Notification.objects.count(), 1)

        # Retrieve the notification and check its attributes.
        notification = Notification.objects.get(message=new_message)
        self.assertEqual(notification.user, self.receiver)
        self.assertEqual(notification.message, new_message)
        self.assertFalse(notification.is_read)
        self.assertEqual(notification.content, f"You have a new message from {self.sender.username}!")

        # Verify that creating another message creates a second notification.
        Message.objects.create(
            sender=self.receiver,
            receiver=self.sender,
            content="Hi back!"
        )

        self.assertEqual(Message.objects.count(), 2)
        self.assertEqual(Notification.objects.count(), 2)

