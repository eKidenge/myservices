from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db import models  # Add this import
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from .models import BlogPost, BlogCategory, BlogComment
from .forms import BlogCommentForm

class BlogListView(ListView):
    """List all blog posts"""
    model = BlogPost
    template_name = 'blog/blog_list.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        queryset = BlogPost.objects.filter(is_published=True)
        
        # Filter by category if specified
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Search functionality
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                models.Q(title__icontains=search_query) |
                models.Q(content__icontains=search_query) |
                models.Q(excerpt__icontains=search_query)
            )
        
        # Filter by tag
        tag = self.request.GET.get('tag')
        if tag:
            queryset = queryset.filter(tags__icontains=tag)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = BlogCategory.objects.filter(is_active=True)
        context['featured_posts'] = BlogPost.objects.filter(
            is_published=True, 
            is_featured=True
        )[:3]
        context['current_category'] = self.request.GET.get('category')
        context['search_query'] = self.request.GET.get('q', '')
        context['current_tag'] = self.request.GET.get('tag', '')
        
        # Get popular tags
        all_tags = []
        for post in BlogPost.objects.filter(is_published=True):
            all_tags.extend(post.get_tags_list())
        context['popular_tags'] = list(set(all_tags))[:10]
        
        return context

class BlogDetailView(DetailView):
    """Blog post detail view"""
    model = BlogPost
    template_name = 'blog/blog_detail.html'
    context_object_name = 'post'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)

    def get(self, request, *args, **kwargs):
        # Increment view count
        self.object = self.get_object()
        self.object.views_count += 1
        self.object.save(update_fields=['views_count'])
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = BlogCommentForm()
        context['comments'] = self.object.comments.filter(is_approved=True)
        
        # Get related posts (same category or similar tags)
        related_posts = BlogPost.objects.filter(
            is_published=True
        ).exclude(id=self.object.id)
        
        if self.object.category:
            related_posts = related_posts.filter(category=self.object.category)
        
        context['related_posts'] = related_posts[:3]
        
        # Get next and previous posts
        context['next_post'] = BlogPost.objects.filter(
            is_published=True,
            published_at__gt=self.object.published_at
        ).order_by('published_at').first()
        
        context['previous_post'] = BlogPost.objects.filter(
            is_published=True,
            published_at__lt=self.object.published_at
        ).order_by('-published_at').first()
        
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = BlogCommentForm(request.POST)
        
        if form.is_valid() and self.object.allow_comments:
            comment = form.save(commit=False)
            comment.post = self.object
            comment.save()
            messages.success(request, 'Your comment has been submitted and is awaiting approval.')
        else:
            messages.error(request, 'There was an error submitting your comment.')
        
        return self.get(request, *args, **kwargs)