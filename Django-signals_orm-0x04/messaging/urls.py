from django.urls import path
from . import views

urlpatterns = [
    path( '', views.index, name='homepage' ),
    path('message/<int:message_id>/history/', views.message_history, name='message_history'),
    path('delete-account/', views.delete_user, name='delete_user'),
]
