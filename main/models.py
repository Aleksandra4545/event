from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Client(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('active', 'Активный'),
        ('completed', 'Завершен'),
        ('archived', 'В архиве'),
    ]
    
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    company = models.CharField(max_length=200, blank=True, verbose_name='Компания')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
    notes = models.TextField(blank=True, verbose_name='Заметки')
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

class Service(models.Model):
    CATEGORY_CHOICES = [
        ('wedding', 'Свадьбы'),
        ('corporate', 'Корпоративы'),
        ('birthday', 'Дни рождения'),
        ('conference', 'Конференции'),
        ('other', 'Другие мероприятия'),
    ]
    
    name = models.CharField(max_length=200, verbose_name='Название услуги')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name='Категория')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    duration_hours = models.IntegerField(verbose_name='Продолжительность (часы)')
    is_available = models.BooleanField(default=True, verbose_name='Доступна')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

class Event(models.Model):
    STATUS_CHOICES = [
        ('planned', 'Запланировано'),
        ('confirmed', 'Подтверждено'),
        ('in_progress', 'В процессе'),
        ('completed', 'Завершено'),
        ('cancelled', 'Отменено'),
    ]
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент')
    name = models.CharField(max_length=200, verbose_name='Название мероприятия')
    event_type = models.CharField(max_length=20, choices=Service.CATEGORY_CHOICES, verbose_name='Тип мероприятия')
    date = models.DateTimeField(verbose_name='Дата и время')
    location = models.CharField(max_length=300, verbose_name='Место проведения')
    budget = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Бюджет')
    guest_count = models.IntegerField(verbose_name='Количество гостей')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    description = models.TextField(blank=True, verbose_name='Описание')
    
    def __str__(self):
        return f"{self.name} - {self.client}"
    
    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'

class EventService(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='Мероприятие')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='Услуга')
    quantity = models.IntegerField(default=1, verbose_name='Количество')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    
    def total_price(self):
        return self.quantity * self.price
    
    class Meta:
        verbose_name = 'Услуга мероприятия'
        verbose_name_plural = 'Услуги мероприятий'

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Низкий'),
        ('medium', 'Средний'),
        ('high', 'Высокий'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='Мероприятие')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    description = models.TextField(blank=True, verbose_name='Описание')
    due_date = models.DateTimeField(verbose_name='Срок выполнения')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium', verbose_name='Приоритет')
    is_completed = models.BooleanField(default=False, verbose_name='Выполнено')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Ответственный')
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'




