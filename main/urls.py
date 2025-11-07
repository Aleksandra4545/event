from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('clients/', views.client_list, name='client_list'),
    path('clients/<int:pk>/', views.client_detail, name='client_detail'),
    path('clients/create/', views.client_create, name='client_create'),
    path('events/', views.event_list, name='event_list'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('services/', views.service_list, name='service_list'),
    path('admin/', admin.site.urls),
]