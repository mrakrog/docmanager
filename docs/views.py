from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category, Tag, Document, DocumentVersion, DocumentAccess
from .serializers import (
    CategorySerializer, TagSerializer, DocumentSerializer,
    DocumentVersionSerializer, DocumentAccessSerializer
)
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly

class CategoryViewSet(viewsets.ModelViewSet):
    """API para gestionar categorías de documentos."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']

    @action(detail=True, methods=['get'])
    def documents(self, request, pk=None):
        """Obtener documentos de una categoría específica."""
        category = self.get_object()
        documents = Document.objects.filter(
            Q(category=category) & (Q(is_public=True) | Q(uploaded_by=request.user))
        )
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)

class TagViewSet(viewsets.ModelViewSet):
    """API para gestionar etiquetas."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    @action(detail=True, methods=['get'])
    def documents(self, request, pk=None):
        """Obtener documentos con una etiqueta específica."""
        tag = self.get_object()
        documents = Document.objects.filter(
            Q(tags=tag) & (Q(is_public=True) | Q(uploaded_by=request.user))
        )
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)

class DocumentViewSet(viewsets.ModelViewSet):
    """API para gestionar documentos."""
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'category__name', 'tags__name']
    ordering_fields = ['title', 'created_at', 'updated_at']

    def get_queryset(self):
        """Filtrar documentos según permisos del usuario."""
        user = self.request.user
        if user.is_staff:
            return Document.objects.all()
        return Document.objects.filter(Q(is_public=True) | Q(uploaded_by=user))

    def perform_create(self, serializer):
        """Asignar el usuario actual como propietario del documento."""
        serializer.save(uploaded_by=self.request.user)

    @action(detail=True, methods=['get'])
    def versions(self, request, pk=None):
        """Obtener versiones de un documento específico."""
        document = self.get_object()
        versions = document.versions.all()
        serializer = DocumentVersionSerializer(versions, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_version(self, request, pk=None):
        """Añadir una nueva versión a un documento."""
        document = self.get_object()
        
        # Determinar el número de versión
        last_version = document.versions.order_by('-version_number').first()
        version_number = 1 if not last_version else last_version.version_number + 1
        
        # Crear datos para la nueva versión
        version_data = {
            'document': document.id,
            'version_number': version_number,
            'notes': request.data.get('notes', ''),
            'file': request.data.get('file')
        }
        
        serializer = DocumentVersionSerializer(data=version_data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """Registrar acceso y devolver URL para descargar el documento."""
        document = self.get_object()
        
        # Registrar el acceso
        DocumentAccess.objects.create(document=document, user=request.user)
        
        # Devolver la URL del archivo
        return Response({'file_url': document.file.url})

class DocumentVersionViewSet(viewsets.ReadOnlyModelViewSet):
    """API para consultar versiones de documentos (solo lectura)."""
    queryset = DocumentVersion.objects.all()
    serializer_class = DocumentVersionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filtrar versiones según permisos del usuario."""
        user = self.request.user
        if user.is_staff:
            return DocumentVersion.objects.all()
        return DocumentVersion.objects.filter(
            Q(document__is_public=True) | Q(document__uploaded_by=user)
        )

class DocumentAccessViewSet(viewsets.ReadOnlyModelViewSet):
    """API para consultar accesos a documentos (solo lectura)."""
    serializer_class = DocumentAccessSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filtrar accesos según permisos del usuario."""
        user = self.request.user
        if user.is_staff:
            return DocumentAccess.objects.all()
        return DocumentAccess.objects.filter(document__uploaded_by=user) 