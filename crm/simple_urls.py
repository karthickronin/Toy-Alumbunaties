from django.urls import path
from . import simple_views as views

app_name = 'crm'

urlpatterns = [
    # Authentication
    path('login/', views.crm_login, name='login'),
    path('logout/', views.crm_logout, name='logout'),
    
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    path('reports/', views.reports, name='reports'),
    
    # Customer Management
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/add/', views.customer_create, name='customer_create'),
    path('customers/<int:customer_id>/', views.customer_detail, name='customer_detail'),
    path('customers/<int:customer_id>/edit/', views.customer_edit, name='customer_edit'),
    path('customers/<int:customer_id>/interaction/', views.add_interaction, name='add_interaction'),
    
    # Booking Management
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/add/', views.booking_create, name='booking_create'),
    path('bookings/add/<int:customer_id>/', views.booking_create, name='booking_create_for_customer'),
    path('bookings/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    
    # Task Management
    path('tasks/', views.task_list, name='task_list'),
]