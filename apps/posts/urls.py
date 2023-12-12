from django.urls import path
from posts import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('create-post', views.create_post, name='create_post'),
    path('detail-post/<int:id>/', views.detail_post, name='detail-post'),
    path('edit_post/<int:id>/', views.edit_post, name='edit_post'),


]