from django.urls import path
from .views import message_history

urlpatterns = [
    path('message/<int:message_id>/history/', message_history, name='message_history'),
]
