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


]