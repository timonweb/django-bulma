from django.views.generic import ListView, FormView

from .forms import FormExample
from .models import Task


class PaginatedList(ListView):
    template_name = 'showcase/paginated_list.html'
    model = Task
    paginate_by = 20


class FormExampleView(FormView):
    template_name = 'showcase/form.html'
    form_class = FormExample
