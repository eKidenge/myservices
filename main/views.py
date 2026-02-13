from django.shortcuts import render
from django.views.generic import TemplateView
from .models import HomePageContent, Testimonial
from services.models import Service
from blog.models import BlogPost

class HomeView(TemplateView):
    """Home page view"""
    template_name = 'main/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_content'] = HomePageContent.objects.filter(is_active=True).first()
        context['testimonials'] = Testimonial.objects.filter(is_active=True)[:5]
        context['featured_services'] = Service.objects.filter(is_active=True)[:6]
        context['latest_posts'] = BlogPost.objects.filter(is_published=True)[:3]
        return context

class AboutView(TemplateView):
    """About page view"""
    template_name = 'main/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testimonials'] = Testimonial.objects.filter(is_active=True)
        return context

class ServicesOverviewView(TemplateView):
    """Services overview page"""
    template_name = 'main/services_overview.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.filter(is_active=True)
        return context