from django.urls import path
from accounts import views

urlpatterns = [
    path('timeout/', views.timeout_view, name='timeout'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
]