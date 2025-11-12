from django.db import models

class Event(models.Model):
    EVENT_TYPES = [
        ('corporate', 'Корпоративное'),
        ('wedding', 'Свадьба'),
        ('birthday', 'День рождения'),
        ('conference', 'Конференция'),
        ('other', 'Другое'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Название мероприятия')
    description = models.TextField(verbose_name='Описание')
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, verbose_name='Тип мероприятия')
    date = models.DateTimeField(verbose_name='Дата и время')
    location = models.CharField(max_length=200, verbose_name='Место проведения')
    budget = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Бюджет')
    client_name = models.CharField(max_length=100, verbose_name='Имя клиента')
    client_phone = models.CharField(max_length=20, verbose_name='Телефон клиента')
    client_email = models.EmailField(verbose_name='Email клиента')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_completed = models.BooleanField(default=False, verbose_name='Завершено')
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'