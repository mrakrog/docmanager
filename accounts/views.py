from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserProfile
from .serializers import UserSerializer, UserProfileSerializer

# Vistas para la API REST
class UserViewSet(viewsets.ModelViewSet):
    """API para gestionar usuarios."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class UserProfileViewSet(viewsets.ModelViewSet):
    """API para gestionar perfiles de usuario."""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filtrar perfiles para que un usuario normal solo vea su propio perfil."""
        user = self.request.user
        if user.is_staff:
            return UserProfile.objects.all()
        return UserProfile.objects.filter(user=user)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def current_user(request):
    """Endpoint para obtener el usuario actual."""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

class RegisterView(APIView):
    """Vista API para registrar nuevos usuarios."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            profile_data = {
                'user': user.id,
                'department': request.data.get('department', ''),
                'position': request.data.get('position', '')
            }
            profile_serializer = UserProfileSerializer(data=profile_data)
            if profile_serializer.is_valid():
                profile_serializer.save()
                return Response(user_serializer.data, status=status.HTTP_201_CREATED)
            user.delete()  # Si el perfil no es válido, eliminar el usuario
            return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vistas para la interfaz web
class RegisterWebView(CreateView):
    """Vista web para el registro de usuarios."""
    template_name = 'accounts/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('accounts:login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Cuenta creada exitosamente. Ahora puedes iniciar sesión.')
        return response

@login_required
def profile_view(request):
    """Vista para el perfil de usuario."""
    return render(request, 'accounts/profile.html', {
        'user': request.user,
        'recent_documents': request.user.uploaded_documents.all()[:5],
        'download_count': 0,  # En una implementación real, calcularía esto
        'last_week_activity': 0  # En una implementación real, calcularía esto
    }) 