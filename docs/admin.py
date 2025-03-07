from django.contrib import admin
from .models import Category, Tag, Document, DocumentVersion, DocumentAccess

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'created_at', 'updated_at')
    list_filter = ('parent', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'uploaded_by', 'is_public', 'created_at', 'updated_at')
    list_filter = ('category', 'is_public', 'created_at', 'tags')
    search_fields = ('title', 'description', 'uploaded_by__username')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('tags',)

@admin.register(DocumentVersion)
class DocumentVersionAdmin(admin.ModelAdmin):
    list_display = ('document', 'version_number', 'created_by', 'created_at')
    list_filter = ('created_at', 'document')
    search_fields = ('document__title', 'notes', 'created_by__username')
    readonly_fields = ('created_at',)

@admin.register(DocumentAccess)
class DocumentAccessAdmin(admin.ModelAdmin):
    list_display = ('document', 'user', 'accessed_at')
    list_filter = ('accessed_at', 'document')
    search_fields = ('document__title', 'user__username')
    readonly_fields = ('accessed_at',) 