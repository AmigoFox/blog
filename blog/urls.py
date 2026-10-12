from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', include('blogs.urls')),
    path('accounts/profile/', lambda request: redirect('blogs:index')),
]
