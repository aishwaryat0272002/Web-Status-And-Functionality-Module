from django.urls import path
from . import views

app_name = 'domains'  # Add this line to avoid namespace conflicts

urlpatterns = [
    path('analyze/', views.analyze_domain, name='analyze_domain'),
    path('phase2/', views.phase2_domain, name='phase2_domain'),
]