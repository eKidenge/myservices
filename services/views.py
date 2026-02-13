from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Service, ServiceCategory

class ServiceListView(ListView):
    """List all services"""
    model = Service
    template_name = 'services/service_list.html'
    context_object_name = 'services'
    paginate_by = 9

    def get_queryset(self):
        queryset = Service.objects.filter(is_active=True)
        
        # Filter by category if specified
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Search functionality
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                models.Q(name__icontains=search_query) |
                models.Q(short_description__icontains=search_query) |
                models.Q(description__icontains=search_query)
            )
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ServiceCategory.objects.filter(is_active=True)
        context['current_category'] = self.request.GET.get('category')
        context['search_query'] = self.request.GET.get('q', '')
        return context

class ServiceDetailView(DetailView):
    """Service detail view"""
    model = Service
    template_name = 'services/service_detail.html'
    context_object_name = 'service'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Service.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get related services from same category
        context['related_services'] = Service.objects.filter(
            category=self.object.category,
            is_active=True
        ).exclude(id=self.object.id)[:3]
        return context