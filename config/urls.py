from django.shortcuts import render
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('', lambda request: render(request, "index.html")),
    path("admin/", admin.site.urls),
    path('api/v1/', include("worker_service.urls")),
    path('api/v1/auth/', include("accounts.urls")),
]
