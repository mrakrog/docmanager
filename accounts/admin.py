from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'position', 'date_joined', 'last_updated')
    search_fields = ('user__username', 'user__email', 'department', 'position')
    list_filter = ('department', 'date_joined')
    readonly_fields = ('date_joined', 'last_updated') 