from django.urls import path, include
from accounts import views

urlpatterns = [
    path('timeout/', views.timeout_view, name='timeout'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('update-my-user/', views.update_my_user, name='update-my-user'),
    path('update-user/<slug:username>/', views.update_user, name='update-user'),
    path('user-list/', views.user_list, name='user_list'),
    path('add-user/', views.add_user, name='add-user'),
    path('new-password/', views.force_password_change_view, name='force_password_change'),
    path("", include("django.contrib.auth.urls")), # Django auth
    
]