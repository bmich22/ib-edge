from django.urls import path
from . import views

urlpatterns = [
    # existing routes...
    path('log_session/', views.log_tutoring_session, name='log_tutoring_session'),
]