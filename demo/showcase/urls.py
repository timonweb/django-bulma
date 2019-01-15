from django.conf.urls import url

from . import views

app_name = 'showcase'
urlpatterns = [
    url(r'^list/$', views.PaginatedList.as_view(), name='paginated_list'),
    url(r'^form/$', views.FormExampleView.as_view(), name='form'),
]
