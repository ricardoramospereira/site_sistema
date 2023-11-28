from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from apps.base import views 

urlpatterns = [
path('admin/', admin.site.urls),
path('base/', views.base_view, name = 'base'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)