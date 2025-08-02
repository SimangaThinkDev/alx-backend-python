from django.shortcuts import render, get_object_or_404
from .models import Message

# Create your views here.

def message_history(request, message_id):
    """
    Renders a page displaying a single message and its edit history.
    """
    # Retrieve the message or return a 404 error if it doesn't exist
    message = get_object_or_404(Message, pk=message_id)
    
    # Retrieve all related MessageHistory objects, ordered by the edited_at timestamp
    history = message.history.all()
    
    context = {
        'message': message,
        'history': history,
    }
    
    return render(request, 'messaging/message_history.html', context)
