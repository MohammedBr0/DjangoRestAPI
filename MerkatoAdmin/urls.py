from django.contrib import admin
from django.urls import path, include  # Import include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('product.urls')), 
    path('', include('CoreUI.urls')), # Include your app's URLs
]
