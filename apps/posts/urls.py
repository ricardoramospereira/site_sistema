from django.urls import path
from posts import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('create-post', views.create_post, name='create_post'),
    path('detail-post/<str:slug>/', views.detail_post, name='detail-post'),
    path('edit_post/<str:slug>/', views.edit_post, name='edit_post'),
    path('delete_post/<str:slug>/', views.delete_post, name='delete_post'),
    path('dashboard/list-post/', views.dash_list_post, name='dash-list-post'),

    # AJAX
    path('remove_image/', views.remove_image, name='remove_image'),

    # Comentários
    path('adicionar-comentario/<str:slug>/', views.adicionar_comentario, name='adicionar-comentario'), #TODO: ALTERAR PARA INGLES
    path('editar-comentario/<int:comentario_id>/', views.editar_comentario, name='editar-comentario'), #TODO: ALTERAR PARA INGLES
    path('deletar-comentario/<int:comentario_id>/', views.deletar_comentario, name='deletar-comentario'),
    path('responder-comentario/<int:comentario_id>/', views.responder_comentario, name='responder-comentario'),

]