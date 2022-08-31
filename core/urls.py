
from django.contrib import admin
from django.urls import path,include

from .views import landing_page_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('insight/',include('insight.urls')),
    path('accounts/',include('accounts.urls')),
    path('',landing_page_view)
]
