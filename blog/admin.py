from django.contrib import admin
from .models import BlogCategory, BlogPost, BlogComment

class BlogCommentInline(admin.TabularInline):
    model = BlogComment
    extra = 0
    readonly_fields = ['name', 'email', 'website', 'comment', 'created_at']
    fields = ['name', 'comment', 'is_approved', 'created_at']
    can_delete = True

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'posts_count', 'created_at']
    list_filter = ['is_active']
    list_editable = ['is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    
    def posts_count(self, obj):
        return obj.posts.count()
    posts_count.short_description = 'Number of Posts'

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'is_published', 'is_featured', 'views_count', 'published_at']
    list_filter = ['is_published', 'is_featured', 'category', 'author']
    list_editable = ['is_published', 'is_featured']
    search_fields = ['title', 'excerpt', 'content', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views_count', 'created_at', 'updated_at']
    date_hierarchy = 'published_at'
    inlines = [BlogCommentInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author', 'category')
        }),
        ('Content', {
            'fields': ('excerpt', 'content', 'featured_image')
        }),
        ('Metadata', {
            'fields': ('tags', 'meta_title', 'meta_description', 'meta_keywords')
        }),
        ('Settings', {
            'fields': ('is_published', 'is_featured', 'allow_comments', 'published_at')
        }),
        ('Statistics', {
            'fields': ('views_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)

@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'post', 'email', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    list_editable = ['is_approved']
    search_fields = ['name', 'email', 'comment']
    readonly_fields = ['name', 'email', 'website', 'comment', 'created_at']  # Removed ip_address
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Comment Information', {
            'fields': ('post', 'name', 'email', 'website')
        }),
        ('Comment', {
            'fields': ('comment',)
        }),
        ('Status', {
            'fields': ('is_approved', 'created_at')
        }),
    )
    
    actions = ['approve_comments', 'disapprove_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = "Approve selected comments"
    
    def disapprove_comments(self, request, queryset):
        queryset.update(is_approved=False)
    disapprove_comments.short_description = "Disapprove selected comments"