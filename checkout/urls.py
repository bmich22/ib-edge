from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('who_is_paying/<int:package_id>/', views.who_is_paying, name='who_is_paying'),
    path('start_checkout/<int:package_id>/', views.start_checkout, name='start_checkout'),
    path('success/', views.checkout_success, name='checkout_success'),
    path('cancel/', views.checkout_cancel, name='checkout_cancel'),
]
