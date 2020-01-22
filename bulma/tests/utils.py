from bs4 import BeautifulSoup
from django.template import engines


def render_template(text, context=None):
    """
    Render template from string
    """
    template = engines["django"].from_string(text)
    if not context:
        context = {}
    return template.render(context)


def render_form(form):
    return render_template(
        """
        {% extends 'bulma/base.html' %}
        {% load bulma_tags %}
        
        {% block content %}
          <form method="post" enctype="multipart/form-data" action="." novalidate>
            {% csrf_token %}
            {{ form|bulma }}
            <button class="button is-primary">Submit</button>
          </form>
        {% endblock %}
        """, context={
            'form': form
        }
    )


def get_dom(html):
    return BeautifulSoup(html, 'html.parser')


def element_has_all_attributes(element, attributes):
    for attribute_name, attribute_value in attributes.items():
        assert element.has_attr(attribute_name) is True
        print(element.get(attribute_name))
        assert element.get(attribute_name) == attribute_value, f'Element {element} has attribute "{attribute_name}" with value {attribute_value}'
            #return False
    #return True


def element_has_attribute(element, attribute_name, attribute_value):
    return element.has_attr(attribute_name) and element.get(attribute_name) == attribute_value
