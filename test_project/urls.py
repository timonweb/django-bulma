"""example URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import path, include
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html')),
    path('login/', LoginView.as_view(), name='login'),
    path('admin/', admin.site.urls),
    path('showcase/', include('showcase.urls', namespace='showcase')),
]
