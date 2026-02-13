from django import forms
from .models import BlogComment

class BlogCommentForm(forms.ModelForm):
    """Form for blog comments"""
    class Meta:
        model = BlogComment
        fields = ['name', 'email', 'website', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
        }