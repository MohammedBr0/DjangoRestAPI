from django.urls import path
from .views import home

urlpatterns = [
    path('', home, name='home'),  # Maps the root URL to the home view
    # Add other URL patterns as needed
]
