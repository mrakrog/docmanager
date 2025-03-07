from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, TagViewSet, DocumentViewSet,
    DocumentVersionViewSet, DocumentAccessViewSet
)
from django.views.generic import TemplateView

# Definir el namespace de la aplicación
app_name = 'docs'

# Configurar router para ViewSets
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'tags', TagViewSet)
router.register(r'documents', DocumentViewSet, basename='document')
router.register(r'versions', DocumentVersionViewSet)
router.register(r'accesses', DocumentAccessViewSet, basename='documentaccess')

urlpatterns = [
    # Incluir rutas automáticas del router
    path('', include(router.urls)),
    
    # URLs temporales para las plantillas hasta que se implementen vistas completas
    path('documents/', TemplateView.as_view(template_name='docs/document_list.html'), name='document_list'),
    path('documents/create/', TemplateView.as_view(template_name='docs/document_form.html'), name='document_create'),
    path('documents/<int:pk>/', TemplateView.as_view(template_name='docs/document_detail.html'), name='document_detail'),
    path('documents/<int:pk>/update/', TemplateView.as_view(template_name='docs/document_form.html'), name='document_update'),
    path('documents/<int:pk>/download/', TemplateView.as_view(template_name='docs/document_detail.html'), name='document_download'),
    path('documents/<int:pk>/add-version/', TemplateView.as_view(template_name='docs/document_form.html'), name='document_add_version'),
    path('documents/<int:pk>/delete/', TemplateView.as_view(), name='document_delete'),
    path('categories/', TemplateView.as_view(), name='category_list'),
    path('categories/<int:pk>/', TemplateView.as_view(), name='category_detail'),
] 