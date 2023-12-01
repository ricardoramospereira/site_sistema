from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include


urlpatterns = [
path('admin/', admin.site.urls),
#path('accounts/', include('django.contrib.auth.urls')),
path('account/', include('accounts.urls')),
path('', include('pages.urls')),
path('profile_user/', include('user_profile.urls')),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)