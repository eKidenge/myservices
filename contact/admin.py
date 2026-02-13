from django.contrib import admin
from .models import ContactMessage
from django.utils.html import format_html

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'service', 'status', 'created_at', 'message_preview']
    list_filter = ['status', 'service', 'created_at']
    list_editable = ['status']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['name', 'email', 'phone', 'subject', 'message', 'service', 
                       'ip_address', 'user_agent', 'created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Sender Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Message Details', {
            'fields': ('subject', 'message', 'service')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Technical Information', {
            'fields': ('ip_address', 'user_agent', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message Preview'
    
    actions = ['mark_as_read', 'mark_as_replied', 'mark_as_archived']
    
    def mark_as_read(self, request, queryset):
        queryset.update(status='read')
    mark_as_read.short_description = "Mark selected as Read"
    
    def mark_as_replied(self, request, queryset):
        queryset.update(status='replied')
    mark_as_replied.short_description = "Mark selected as Replied"
    
    def mark_as_archived(self, request, queryset):
        queryset.update(status='archived')
    mark_as_archived.short_description = "Archive selected"
    
    def has_add_permission(self, request):
        # Disable adding messages manually
        return False