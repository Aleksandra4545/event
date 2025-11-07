from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count, Sum
from django.contrib import messages
from .models import Client, Service, Event, Task
from .forms import ClientForm, ServiceForm, EventForm, TaskForm

def home(request):
    """Главная страница"""
    services = Service.objects.filter(is_available=True)[:6]
    recent_events = Event.objects.select_related('client').order_by('-created_at')[:3]
    
    context = {
        'services': services,
        'recent_events': recent_events,
    }
    return render(request, 'home.html', context)

@login_required
def dashboard(request):
    """Панель управления"""
    # Статистика
    total_clients = Client.objects.count()
    total_events = Event.objects.count()
    active_events = Event.objects.filter(status__in=['planned', 'confirmed', 'in_progress']).count()
    total_revenue = Event.objects.aggregate(Sum('budget'))['budget__sum'] or 0
    
    # Ближайшие мероприятия
    upcoming_events = Event.objects.filter(
        status__in=['planned', 'confirmed']
    ).select_related('client').order_by('date')[:5]
    
    # Предстоящие задачи
    upcoming_tasks = Task.objects.filter(
        is_completed=False
    ).select_related('event', 'assigned_to').order_by('due_date')[:10]
    
    context = {
        'total_clients': total_clients,
        'total_events': total_events,
        'active_events': active_events,
        'total_revenue': total_revenue,
        'upcoming_events': upcoming_events,
        'upcoming_tasks': upcoming_tasks,
    }
    return render(request, 'dashboard.html', context)

@login_required
def client_list(request):
    """Список клиентов"""
    clients = Client.objects.all().order_by('-created_at')
    
    # Фильтрация
    status_filter = request.GET.get('status')
    if status_filter:
        clients = clients.filter(status=status_filter)
    
    # Поиск
    search_query = request.GET.get('search')
    if search_query:
        clients = clients.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(company__icontains=search_query)
        )
    
    context = {
        'clients': clients,
        'status_choices': Client.STATUS_CHOICES,
    }
    return render(request, 'clients/client_list.html', context)

@login_required
def client_detail(request, pk):
    """Детальная информация о клиенте"""
    client = get_object_or_404(Client, pk=pk)
    events = client.event_set.all().order_by('-date')
    
    context = {
        'client': client,
        'events': events,
    }
    return render(request, 'clients/client_detail.html', context)

@login_required
def client_create(request):
    """Создание нового клиента"""
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save()
            messages.success(request, f'Клиент {client} успешно создан!')
            return redirect('client_detail', pk=client.pk)
    else:
        form = ClientForm()
    
    context = {'form': form}
    return render(request, 'clients/client_form.html', context)

@login_required
def event_list(request):
    """Список мероприятий"""
    events = Event.objects.select_related('client').all().order_by('-date')
    
    # Фильтрация
    status_filter = request.GET.get('status')
    if status_filter:
        events = events.filter(status=status_filter)
    
    type_filter = request.GET.get('type')
    if type_filter:
        events = events.filter(event_type=type_filter)
    
    context = {
        'events': events,
        'status_choices': Event.STATUS_CHOICES,
        'type_choices': Service.CATEGORY_CHOICES,
    }
    return render(request, 'events/event_list.html', context)

@login_required
def event_detail(request, pk):
    """Детальная информация о мероприятии"""
    event = get_object_or_404(Event.objects.select_related('client'), pk=pk)
    services = event.eventservice_set.select_related('service')
    tasks = event.task_set.select_related('assigned_to')
    
    context = {
        'event': event,
        'services': services,
        'tasks': tasks,
    }
    return render(request, 'events/event_detail.html', context)

@login_required
def service_list(request):
    """Список услуг"""
    services = Service.objects.all().order_by('category', 'name')
    
    # Фильтрация по категории
    category_filter = request.GET.get('category')
    if category_filter:
        services = services.filter(category=category_filter)
    
    context = {
        'services': services,
        'category_choices': Service.CATEGORY_CHOICES,
    }
    return render(request, 'services/service_list.html', context)

