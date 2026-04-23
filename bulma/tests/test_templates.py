from django.core.paginator import Paginator

from bulma.tests.forms import FormExample
from bulma.tests.utils import get_dom, render_template


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


def test_pagination_highlights_only_current_page():
    paginator = Paginator(range(1, 51), 10)  # 50 items, 5 pages
    page_obj = paginator.get_page(3)

    output = render_template(
        "{% include 'pagination.html' %}",
        context={
            'is_paginated': True,
            'paginator': paginator,
            'page_obj': page_obj,
            'getvars': '',
            'hashtag': '',
        }
    )

    dom = get_dom(output)
    links = dom.select('a.pagination-link')

    assert len(links) == 5, "Should render 5 page links"

    current_links = [link for link in links if 'is-current' in link.get('class', [])]
    assert len(current_links) == 1, "Only one page should be marked as current"
    assert current_links[0].text.strip() == '3', "Page 3 should be the current page"
