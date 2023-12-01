from django.urls import path
from config import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('settings/', views.config_view, name='settings'),
]