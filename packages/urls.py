from django.urls import path
from . import views

urlpatterns = [
    path('', views.packages, name='packages'),
    path('', views.package_list, name='package_list'),
]
