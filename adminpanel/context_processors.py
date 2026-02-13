from .models import SiteSettings

def site_settings(request):
    """Add site settings to template context"""
    return {
        'site_settings': SiteSettings.load()
    }