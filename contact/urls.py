from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    path('', views.ContactFormView.as_view(), name='form'),
    path('success/', views.ContactSuccessView.as_view(), name='success'),
]