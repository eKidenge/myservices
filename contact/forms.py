from django import forms
from .models import ContactMessage
from services.models import Service

class ContactForm(forms.ModelForm):
    """Contact form"""
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message', 'service']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'].queryset = Service.objects.filter(is_active=True)
        self.fields['service'].empty_label = "Select a service (optional)"
        self.fields['phone'].required = False