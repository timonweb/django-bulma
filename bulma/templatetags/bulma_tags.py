# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
from math import floor

from django import forms
from django.template.loader import get_template
from django import template
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe

from ..bulma import (css_url, font_awesome_url)
from ..utils import (render_link_tag, url_replace_param)
# from ..text import force_text

register = template.Library()

BULMA_COLUMN_COUNT = 1


@register.filter
def bulma(element):
    markup_classes = {'label': '', 'value': '', 'single_value': ''}
    return render(element, markup_classes)


@register.filter
def bulma_inline(element):
    markup_classes = {'label': 'sr-only', 'value': '', 'single_value': ''}
    return render(element, markup_classes)


@register.filter
def bulma_horizontal(element, label_cols='is-2'):
    markup_classes = {'label': label_cols, 'value': '', 'single_value': ''}

    for cl in label_cols.split(' '):
        splitted_class = cl.split('-')

        try:
            value_nb_cols = int(splitted_class[-1])
        except ValueError:
            value_nb_cols = BULMA_COLUMN_COUNT

        if value_nb_cols >= BULMA_COLUMN_COUNT:
            splitted_class[-1] = str(BULMA_COLUMN_COUNT)
        else:
            offset_class = cl.split('-')
            offset_class[-1] = 'offset-' + str(value_nb_cols)
            splitted_class[-1] = str(BULMA_COLUMN_COUNT - value_nb_cols)
            markup_classes['single_value'] += ' ' + '-'.join(offset_class)
            markup_classes['single_value'] += ' ' + '-'.join(splitted_class)

        markup_classes['value'] += ' ' + '-'.join(splitted_class)

    return render(element, markup_classes)


@register.filter
def add_input_classes(field):
    if not is_checkbox(field) and not is_multiple_checkbox(field) \
            and not is_radio(field) and not is_file(field):
        field_classes = field.field.widget.attrs.get('class', '')
        field_classes += ' control'
        field.field.widget.attrs['class'] = field_classes


def render(element, markup_classes):
    element_type = element.__class__.__name__.lower()

    if element_type == 'boundfield':
        add_input_classes(element)
        template = get_template("bulma/forms/field.html")
        context = {'field': element, 'classes': markup_classes, 'form': element.form}
    else:
        has_management = getattr(element, 'management_form', None)
        if has_management:
            for form in element.forms:
                for field in form.visible_fields():
                    add_input_classes(field)

            template = get_template("bulma/forms/formset.html")
            context = {'formset': element, 'classes': markup_classes}
        else:
            for field in element.visible_fields():
                add_input_classes(field)

            template = get_template("bulma/forms/form.html")
            context = {'form': element, 'classes': markup_classes}

    return template.render(context)


@register.filter
def widget_type(field):
    return field.field.widget


@register.filter
def is_select(field):
    return isinstance(field.field.widget, forms.Select)


@register.filter
def is_multiple_select(field):
    return isinstance(field.field.widget, forms.SelectMultiple)


@register.filter
def is_textarea(field):
    return isinstance(field.field.widget, forms.Textarea)


@register.filter
def is_input(field):
    return isinstance(field.field.widget, (
        forms.TextInput,
        forms.NumberInput,
        forms.EmailInput,
        forms.PasswordInput,
        forms.URLInput
    ))


@register.filter
def is_checkbox(field):
    return isinstance(field.field.widget, forms.CheckboxInput)


@register.filter
def is_multiple_checkbox(field):
    return isinstance(field.field.widget, forms.CheckboxSelectMultiple)


@register.filter
def is_radio(field):
    return isinstance(field.field.widget, forms.RadioSelect)


@register.filter
def is_file(field):
    return isinstance(field.field.widget, forms.FileInput)


@register.filter
def addclass(field, css_class):
    if len(field.errors) > 0:
        css_class += ' is-danger'
    return field.as_widget(attrs={"class": css_class})


@register.filter
def bulma_message_tag(tag):
    return {
        'error': 'danger'
    }.get(tag, tag)


@register.simple_tag
def bulma_css_url():
    """
    Return the full url to the Bulma CSS library
    Default value: ``None``
    This value is configurable, see Settings section
    **Tag name**::
        bulma_css_url
    **Usage**::
        {% bulma_css_url %}
    **Example**::
        {% bulma_css_url %}
    """
    return css_url()


@register.simple_tag
def bulma_css():
    """
    Return HTML for Bulma CSS.
    Adjust url in settings. If no url is returned, we don't want this statement
    to return any HTML.
    This is intended behavior.
    Default value: ``None``
    This value is configurable, see Settings section
    **Tag name**::
        bulma_css
    **Usage**::
        {% bulma_css %}
    **Example**::
        {% bulma_css %}
    """
    rendered_urls = [render_link_tag(bulma_css_url()), ]
    if font_awesome_url():
        rendered_urls.append(render_link_tag(font_awesome_url()))
    return mark_safe(''.join([url for url in rendered_urls]))


@register.inclusion_tag('pagination.html')
def bulma_pagination(page, **kwargs):
    """
    Render pagination for a page
    **Tag name**::
        bulma_pagination
    **Parameters**:
        page
            The page of results to show.
        pages_to_show
            Number of pages in total
            :default: ``11``
        url
            URL to navigate to for pagination forward and pagination back.
            :default: ``None``
        size
            Controls the size of the pagination through CSS.
            Defaults to being normal sized.
            One of the following:
                * ``'small'``
                * ``'large'``
            :default: ``None``
        extra
            Any extra page parameters.
            :default: ``None``
        parameter_name
            Name of the paging URL parameter.
            :default: ``'page'``
    **Usage**::
        {% bulma_pagination page %}
    **Example**::
        {% bulma_pagination lines url="/pagination?page=1" size="large" %}
        {% bulma_pagination page_obj extra=request.GET.urlencode %}
    """

    pagination_kwargs = kwargs.copy()
    pagination_kwargs['page'] = page
    return get_pagination_context(**pagination_kwargs)


@register.simple_tag
def bulma_url_replace_param(url, name, value):
    return url_replace_param(url, name, value)


def get_pagination_context(page, pages_to_show=11,
                           url=None, size=None, extra=None,
                           parameter_name='page'):
    """
    Generate Bulma pagination context from a page object
    """
    pages_to_show = int(pages_to_show)
    if pages_to_show < 1:
        raise ValueError(
            "Pagination pages_to_show should be a positive integer, you specified {pages}".format(
                pages=pages_to_show)
        )
    num_pages = page.paginator.num_pages
    current_page = page.number
    half_page_num = int(floor(pages_to_show / 2))
    if half_page_num < 0:
        half_page_num = 0
    first_page = current_page - half_page_num
    if first_page <= 1:
        first_page = 1
    if first_page > 1:
        pages_back = first_page - half_page_num
        if pages_back < 1:
            pages_back = 1
    else:
        pages_back = None
    last_page = first_page + pages_to_show - 1
    if pages_back is None:
        last_page += 1
    if last_page > num_pages:
        last_page = num_pages
    if last_page < num_pages:
        pages_forward = last_page + half_page_num
        if pages_forward > num_pages:
            pages_forward = num_pages
    else:
        pages_forward = None
        if first_page > 1:
            first_page -= 1
        if pages_back is not None and pages_back > 1:
            pages_back -= 1
        else:
            pages_back = None
    pages_shown = []
    for i in range(first_page, last_page + 1):
        pages_shown.append(i)
        # Append proper character to url
    if url:
        # Remove existing page GET parameters
        url = force_text(url)
        url = re.sub(r'\?{0}\=[^\&]+'.format(parameter_name), '?', url)
        url = re.sub(r'\&{0}\=[^\&]+'.format(parameter_name), '', url)
        # Append proper separator
        if '?' in url:
            url += '&'
        else:
            url += '?'
            # Append extra string to url
    if extra:
        if not url:
            url = '?'
        url += force_text(extra) + '&'
    if url:
        url = url.replace('?&', '?')
    # Set CSS classes, see https://bulma.io/documentation/components/pagination/
    pagination_css_classes = ['pagination', 'is-centered']
    if size == 'small':
        pagination_css_classes.append('is-small')
    elif size == 'large':
        pagination_css_classes.append('is-large')
        # Build context object
    return {
        'bulma_pagination_url': url,
        'num_pages': num_pages,
        'current_page': current_page,
        'first_page': first_page,
        'last_page': last_page,
        'pages_shown': pages_shown,
        'pages_back': pages_back,
        'pages_forward': pages_forward,
        'pagination_css_classes': ' '.join(pagination_css_classes),
        'parameter_name': parameter_name,
    }
