"""
URL Configuration for docmanager project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.defaults import server_error, page_not_found, permission_denied
from django.http import HttpResponse

# Vista simple para verificar que Django está funcionando
def health_check(request):
    return HttpResponse("OK - Servidor funcionando correctamente", content_type="text/plain")

urlpatterns = [
    # Vista de diagnóstico
    path('health/', health_check, name='health_check'),
    
    # Admin panel
    path('admin/', admin.site.urls),
    
    # API endpoints - todas las rutas de API empiezan con /api/
    path('api/accounts/', include('accounts.urls', namespace='api_accounts')),
    path('api/docs/', include('docs.urls', namespace='api_docs')),
    
    # Páginas web (interfaces de usuario)
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('docs/', include('docs.urls', namespace='docs')),
    
    # Ruta principal para la aplicación frontend
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    
    # Rutas de prueba para errores
    path('500/', server_error),
    path('404/', page_not_found, {'exception': Exception("Página no encontrada")}),
    path('403/', permission_denied, {'exception': Exception("Permiso denegado")}),
]

# Servir archivos estáticos y media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 