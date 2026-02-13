from django.db import models
from django.utils import timezone

class HomePageContent(models.Model):
    """Model for homepage content"""
    hero_title = models.CharField(max_length=200)
    hero_subtitle = models.TextField()
    hero_image = models.ImageField(upload_to='home/', blank=True, null=True)
    about_section_title = models.CharField(max_length=200)
    about_section_content = models.TextField()
    about_section_image = models.ImageField(upload_to='home/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Home Page Content"
        verbose_name_plural = "Home Page Contents"

    def __str__(self):
        return f"Homepage Content - {self.updated_at.date()}"

class Testimonial(models.Model):
    """Model for testimonials shown on homepage"""
    author_name = models.CharField(max_length=100)
    author_position = models.CharField(max_length=100, blank=True)
    author_image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    content = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Testimonial by {self.author_name}"