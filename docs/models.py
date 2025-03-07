from django.db import models
from django.contrib.auth.models import User
import os

class Category(models.Model):
    """Modelo para categorías de documentos."""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

class Tag(models.Model):
    """Modelo para etiquetas de documentos."""
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

def document_upload_path(instance, filename):
    """Función para determinar la ruta de subida de documentos."""
    # Obtener la extensión del archivo
    ext = filename.split('.')[-1]
    # Crear un nombre de archivo basado en el título del documento
    filename = f"{instance.title.replace(' ', '_').lower()}.{ext}"
    # Devolver la ruta completa
    return os.path.join('documents', str(instance.category.id), filename)

class Document(models.Model):
    """Modelo principal para documentos."""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to=document_upload_path)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='documents')
    tags = models.ManyToManyField(Tag, blank=True, related_name='documents')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_documents')
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']

class DocumentVersion(models.Model):
    """Modelo para versiones de documentos."""
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='versions')
    file = models.FileField(upload_to='document_versions/')
    version_number = models.PositiveIntegerField()
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.document.title} - v{self.version_number}"
    
    class Meta:
        ordering = ['-version_number']
        unique_together = ['document', 'version_number']

class DocumentAccess(models.Model):
    """Modelo para registrar accesos a documentos."""
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='accesses')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    accessed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} accessed {self.document.title} at {self.accessed_at}"
    
    class Meta:
        ordering = ['-accessed_at']
        verbose_name_plural = 'Document Accesses' 