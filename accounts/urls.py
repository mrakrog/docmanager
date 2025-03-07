from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserProfileViewSet, current_user, RegisterView, RegisterWebView, profile_view
from rest_framework.authtoken.views import obtain_auth_token
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

# Definir el namespace de la aplicación
app_name = 'accounts'

# Configurar router para ViewSets
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', UserProfileViewSet)

# URLs temporales para plantillas hasta que se implementen las vistas completas
urlpatterns = [
    # Incluir rutas automáticas del router
    path('api/', include(router.urls)),
    
    # Rutas personalizadas para la API
    path('api/me/', current_user, name='current-user'),
    path('api/register/', RegisterView.as_view(), name='api-register'),
    path('api/token-auth/', obtain_auth_token, name='api-token-auth'),
    
    # URLs para las páginas web (no API)
    path('register/', RegisterWebView.as_view(), name='register'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', TemplateView.as_view(template_name='accounts/profile.html'), name='profile_edit'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
] 