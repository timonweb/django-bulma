from django.urls import path

from . import views

app_name = "showcase"
urlpatterns = [
    path("list/", views.PaginatedList.as_view(), name="paginated_list"),
    path("form/", views.FormExampleView.as_view(), name="form"),
]
