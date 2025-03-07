from rest_framework import serializers
from .models import Category, Tag, Document, DocumentVersion, DocumentAccess
from django.contrib.auth.models import User

class UserMinimalSerializer(serializers.ModelSerializer):
    """Serializador mínimo para usuarios."""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

class CategorySerializer(serializers.ModelSerializer):
    """Serializador para categorías."""
    children = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'parent', 'children', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def get_children(self, obj):
        """Obtener categorías hijas."""
        children = Category.objects.filter(parent=obj)
        serializer = CategoryMinimalSerializer(children, many=True)
        return serializer.data

class CategoryMinimalSerializer(serializers.ModelSerializer):
    """Serializador mínimo para categorías (evita recursión infinita)."""
    class Meta:
        model = Category
        fields = ['id', 'name']

class TagSerializer(serializers.ModelSerializer):
    """Serializador para etiquetas."""
    class Meta:
        model = Tag
        fields = ['id', 'name']

class DocumentVersionSerializer(serializers.ModelSerializer):
    """Serializador para versiones de documentos."""
    created_by = UserMinimalSerializer(read_only=True)
    
    class Meta:
        model = DocumentVersion
        fields = ['id', 'document', 'file', 'version_number', 'notes', 'created_by', 'created_at']
        read_only_fields = ['created_at']

class DocumentSerializer(serializers.ModelSerializer):
    """Serializador para documentos."""
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), 
        source='category',
        write_only=True
    )
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        source='tags',
        write_only=True,
        many=True,
        required=False
    )
    uploaded_by = UserMinimalSerializer(read_only=True)
    versions_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = [
            'id', 'title', 'description', 'file', 'category', 'category_id',
            'tags', 'tag_ids', 'uploaded_by', 'is_public', 'created_at', 
            'updated_at', 'versions_count'
        ]
        read_only_fields = ['created_at', 'updated_at', 'uploaded_by']
    
    def get_versions_count(self, obj):
        """Obtener el número de versiones del documento."""
        return obj.versions.count()
    
    def create(self, validated_data):
        """Crear un nuevo documento con etiquetas."""
        tags = validated_data.pop('tags', [])
        document = Document.objects.create(**validated_data)
        if tags:
            document.tags.set(tags)
        return document
    
    def update(self, instance, validated_data):
        """Actualizar un documento existente."""
        tags = validated_data.pop('tags', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if tags is not None:
            instance.tags.set(tags)
        
        return instance

class DocumentAccessSerializer(serializers.ModelSerializer):
    """Serializador para accesos a documentos."""
    user = UserMinimalSerializer(read_only=True)
    document = serializers.StringRelatedField()
    
    class Meta:
        model = DocumentAccess
        fields = ['id', 'document', 'user', 'accessed_at']
        read_only_fields = ['accessed_at'] 