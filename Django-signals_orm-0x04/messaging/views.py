from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Prefetch # Import Prefetch for nested prefetching
from .models import Message

@login_required
def inbox_optimized(request):
    """
    View to display a user's inbox, optimized with select_related and prefetch_related.
    It fetches all top-level messages and their replies in a minimal number of queries.
    """
    # Fetch top-level messages where the user is either the sender or the receiver.
    # .select_related('sender', 'receiver') joins the User table for both sender and receiver
    # in the initial query, preventing an N+1 query problem for those fields.
    # .prefetch_related('replies') fetches all replies for the top-level messages
    # in a single subsequent query, which also avoids the N+1 problem.
    messages = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user),
        parent_message__isnull=True
    ).select_related(
        'sender', 'receiver'
    ).prefetch_related(
        Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver').order_by('-timestamp'))
    ).order_by('-timestamp')

    context = {
        'messages': messages,
    }
    return render(request, 'messaging/inbox_optimized.html', context)

@login_required
def inbox_unread(request):
    """
    View to display only the unread messages for the logged-in user.
    """
    # Use the custom manager and optimize the query with .select_related() and .only()
    unread_messages = Message.unread.unread_for_user(request.user).select_related('sender').only(
        'content', 'timestamp', 'sender',
    )

    context = {
        'unread_messages': unread_messages,
    }
    return render(request, 'messaging/inbox_unread.html', context)

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

def build_reply_tree(message):
    """
    Recursively fetches all replies for a given message.
    """
    # Fetch replies for the current message and prefetch their own replies.
    replies = message.replies.select_related('sender', 'receiver').order_by('timestamp').prefetch_related('replies')
    
    # Recursively build the tree for each reply.
    for reply in replies:
        reply.replies_tree = build_reply_tree(reply)
        
    return list(replies)

@login_required
def message_thread(request, message_id):
    """
    View to display a full message thread in a recursive format.
    """
    message = get_object_or_404(Message.objects.select_related('sender', 'receiver'), pk=message_id)
    
    # Build the full thread tree for the message.
    thread_tree = build_reply_tree(message)
    
    context = {
        'message': message,
        'thread_tree': thread_tree,
    }
    
    return render(request, 'messaging/message_thread.html', context)
