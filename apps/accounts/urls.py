from django.urls import path
from accounts import views

urlpatterns = [
    path('timeout/', views.timeout_view, name='timeout')
]