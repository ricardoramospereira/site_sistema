from django.urls import path
from user_profile import views

urlpatterns = [
    path('<slug:username>/', views.perfil_view, name='perfil_view'),
    path('editar-perfil/<slug:username>/', views.editar_perfil, name='editar_perfil'),

]