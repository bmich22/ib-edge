from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.contact, name='contact'),
    path('success/', TemplateView.as_view(
        template_name='contacts/contact_success.html'),
        name='contact_success'),
]
