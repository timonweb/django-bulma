from django.urls import re_path as url, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='home.html')),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^admin/', admin.site.urls),
    url(r'^showcase/', include('showcase.urls', namespace='showcase')),
]
