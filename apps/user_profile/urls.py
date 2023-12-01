from django.urls import path
from user_profile import views

urlpatterns = [
    path('<slug:username>/', views.perfil_view, name='perfil_view')
]