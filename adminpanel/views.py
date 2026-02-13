from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Count, Q
from datetime import datetime, timedelta
from services.models import Service
from blog.models import BlogPost
from contact.models import ContactMessage

class AdminDashboardView(UserPassesTestMixin, TemplateView):
    """Admin dashboard view"""
    template_name = 'adminpanel/admin_dashboard.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Statistics
        context['total_services'] = Service.objects.count()
        context['active_services'] = Service.objects.filter(is_active=True).count()
        
        context['total_posts'] = BlogPost.objects.count()
        context['published_posts'] = BlogPost.objects.filter(is_published=True).count()
        
        context['total_messages'] = ContactMessage.objects.count()
        context['new_messages'] = ContactMessage.objects.filter(status='new').count()
        
        # Recent messages
        context['recent_messages'] = ContactMessage.objects.order_by('-created_at')[:5]
        
        # Recent posts
        context['recent_posts'] = BlogPost.objects.order_by('-created_at')[:5]
        
        # Chart data for last 30 days
        last_30_days = datetime.now() - timedelta(days=30)
        
        # Messages by day
        messages_by_day = ContactMessage.objects.filter(
            created_at__gte=last_30_days
        ).extra({
            'day': "date(created_at)"
        }).values('day').annotate(count=Count('id')).order_by('day')
        
        context['messages_chart_data'] = list(messages_by_day)
        
        return context