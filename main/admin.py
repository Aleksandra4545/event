from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'date', 'client_name', 'budget', 'is_completed']
    list_filter = ['event_type', 'is_completed', 'date']
    search_fields = ['title', 'client_name', 'client_email']