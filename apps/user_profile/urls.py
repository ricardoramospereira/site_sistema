from django.urls import path
from user_profile import views

urlpatterns = [
    path('<int:id>/', views.perfil_view, name='perfil_view')
]