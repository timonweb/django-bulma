from bulma.tests.forms import FormExample
from bulma.tests.utils import render_template


def test_bulma_base_template():
    output = render_template(
        """
        {% extends 'bulma/base.html' %}
        {% block content %}
            test_bulma_content
        {% endblock content %}
        """
    )

    assert "test_bulma_content" in output, "Content is in template"


def test_style_css_is_in_template():
    output = render_template(
        """
        {% extends 'bulma/base.html' %}
        """
    )
    assert '<link rel="stylesheet" href="/static/bulma/css/style.min.css">' in output


def test_bulma_form_tag():
    output = render_template(
        """
        {% extends 'bulma/base.html' %}
        {% load bulma_tags %}
        {% block content %}
            <form>{{ form|bulma }}</form>
        {% endblock content %}
        """, context={
            'form': FormExample()
        }
    )

    assert '<div class="field"' in output, "Fields are rendered"
