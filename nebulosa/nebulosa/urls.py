from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from boletos import views

urlpatterns = [
    path('', views.lista_boletos, name='home'),
    path('admin/', admin.site.urls),
    path('boletos/', include('boletos.urls')),

    # Login personalizado
    path(
        'accounts/login/',
        auth_views.LoginView.as_view(template_name='boletos/login.html'),
        name='login'
    ),

    # Resto de URLs de auth (logout, reset, etc.)
    path('accounts/', include('django.contrib.auth.urls')),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
