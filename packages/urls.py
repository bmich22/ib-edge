from django.urls import path
from . import views

urlpatterns = [
    path('', views.packages, name='packages'),
    path('add/', views.add_package, name='add_package'),
    path('edit/<int:package_id>/', views.edit_package, name='edit_package'),
    path('delete/<int:package_id>/', views.delete_package, name='delete_package'),
]
