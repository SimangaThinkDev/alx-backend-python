from django.shortcuts import render, get_object_or_404, redirect
from .models import Message
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render( request, 'messaging/index.html' )


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


@login_required
def delete_user(request):
    """
    View to handle the deletion of a user's account.
    """
    if request.method == 'POST':
        # Get the currently logged-in user
        user = request.user
        
        # Log the user out before deleting the account
        logout(request)
        
        # Delete the user's account
        user.delete()
        
        # Redirect to the homepage or a confirmation page
        return redirect('homepage')  # Assuming you have a 'homepage' URL name
    
    # If the request is a GET, display a confirmation page
    return render(request, 'messaging/delete_account_confirm.html')


@login_required
def inbox_unread(request):
    """
    View to display only the unread messages for the logged-in user.
    """
    # Use the custom manager and optimize the query with .select_related() and .only()
    unread_messages = Message.objects.unread_for_user(request.user).select_related('sender').only(
        'content', 'timestamp', 'sender',
    )

    context = {
        'unread_messages': unread_messages,
    }
    return render(request, 'messaging/inbox_unread.html', context)

