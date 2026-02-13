from django.contrib import admin
from .models import HomePageContent, Testimonial

@admin.register(HomePageContent)
class HomePageContentAdmin(admin.ModelAdmin):
    list_display = ['hero_title', 'is_active', 'updated_at']
    list_editable = ['is_active']
    fieldsets = (
        ('Hero Section', {
            'fields': ('hero_title', 'hero_subtitle', 'hero_image')
        }),
        ('About Section', {
            'fields': ('about_section_title', 'about_section_content', 'about_section_image')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

    def has_add_permission(self, request):
        # Only allow one homepage content
        if HomePageContent.objects.exists():
            return False
        return super().has_add_permission(request)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'rating', 'is_active', 'created_at']
    list_filter = ['rating', 'is_active']
    list_editable = ['is_active']
    search_fields = ['author_name', 'content']
    date_hierarchy = 'created_at'