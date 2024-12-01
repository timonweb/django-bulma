from django.urls import include, path
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html")),
    path("login/", LoginView.as_view(), name="login"),
    path("admin/", admin.site.urls),
    path("showcase/", include("showcase.urls", namespace="showcase")),
]
