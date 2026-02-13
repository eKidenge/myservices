from django.shortcuts import render, redirect
from django.views.generic import FormView, TemplateView  # Add TemplateView here
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from .models import ContactMessage

class ContactFormView(FormView):
    """Contact form view"""
    template_name = 'contact/contact_form.html'
    form_class = ContactForm
    success_url = '/contact/success/'

    def form_valid(self, form):
        # Save the message
        contact_message = form.save(commit=False)
        
        # Capture IP and user agent
        contact_message.ip_address = self.get_client_ip()
        contact_message.user_agent = self.request.META.get('HTTP_USER_AGENT', '')
        contact_message.save()
        
        # Send email notification
        self.send_email_notification(contact_message)
        
        messages.success(self.request, 'Your message has been sent successfully! We will get back to you soon.')
        return super().form_valid(form)

    def get_client_ip(self):
        """Get client IP address"""
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

    def send_email_notification(self, contact_message):
        """Send email notification"""
        subject = f"New Contact Form Message: {contact_message.subject}"
        message = f"""
        New message from {contact_message.name} ({contact_message.email})
        
        Subject: {contact_message.subject}
        
        Message:
        {contact_message.message}
        
        Phone: {contact_message.phone or 'Not provided'}
        Service: {contact_message.service.name if contact_message.service else 'Not specified'}
        """
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],
                fail_silently=False,
            )
        except:
            # Log error but don't stop the process
            pass

class ContactSuccessView(TemplateView):
    """Contact form success view"""
    template_name = 'contact/contact_success.html'