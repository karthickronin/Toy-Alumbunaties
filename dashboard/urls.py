from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('login/', views.dashboard_login, name='login'),
    path('logout/', views.dashboard_logout, name='logout'),
    path('content/', views.content_management, name='content'),
    path('portfolio/', views.portfolio_management, name='portfolio'),
    path('inquiries/', views.inquiry_management, name='inquiries'),
    path('team/', views.team_management, name='team'),
]