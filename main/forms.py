from django import forms
from .models import Client, Service, Event, Task

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'email', 'phone', 'company', 'status', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'category', 'description', 'price', 'duration_hours', 'is_available']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['client', 'name', 'event_type', 'date', 'location', 'budget', 'guest_count', 'status', 'description']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['event', 'title', 'description', 'due_date', 'priority', 'assigned_to']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }