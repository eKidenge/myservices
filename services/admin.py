from django.contrib import admin
from .models import ServiceCategory, Service

class ServiceInline(admin.TabularInline):
    model = Service
    extra = 1
    fields = ['name', 'price', 'is_featured', 'is_active']

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'service_count', 'created_at']
    list_filter = ['is_active']
    list_editable = ['is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ServiceInline]
    
    def service_count(self, obj):
        return obj.services.count()
    service_count.short_description = 'Number of Services'

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_featured', 'is_active', 'created_at']
    list_filter = ['category', 'is_featured', 'is_active']
    list_editable = ['is_featured', 'is_active']
    search_fields = ['name', 'short_description', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_select_related = ['category']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('category', 'name', 'slug', 'icon')
        }),
        ('Description', {
            'fields': ('short_description', 'description', 'features')
        }),
        ('Media & Pricing', {
            'fields': ('image', 'price')
        }),
        ('Status', {
            'fields': ('is_featured', 'is_active')
        }),
    )