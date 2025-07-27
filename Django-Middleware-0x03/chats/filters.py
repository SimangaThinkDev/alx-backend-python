from django_filters import rest_framework as filters
from django.utils import timezone
from datetime import timedelta
from .models import Message


class MessageFilter(filters.FilterSet):
    created_at = filters.NumberFilter(
        field_name="time_stamp",
        method="get_past_n_hours",
        label="Past n hours",
    )

    def get_past_n_hours(self, queryset, field_name, value):
        time_threshold = timezone.now() - timedelta(hours=int(value))
        return queryset.filter(time_stamp__gte=time_threshold)

    class Meta:
        model = Message
        fields = ("created_at", "sender")
