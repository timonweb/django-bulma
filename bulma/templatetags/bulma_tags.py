from django import forms, template
from django.template.base import FilterExpression
from django.template.library import SimpleNode
from django.template.loader import get_template
from django.utils.safestring import mark_safe

from bulma.types import InputSizesStr
from bulma.utils import css_class_string

register = template.Library()


@register.simple_tag
def bulma_label(field, template_name="bulma/forms/field_label.html"):
    return get_template(template_name).render({"field": field})


@register.simple_tag
def bulma_field(
    field,
    inline: bool = False,
    control_only: bool = False,
    is_horizontal: bool = False,
    field_label_size: str = "is-normal",
    icon_left: str = None,
    icon_left_size: str = "is-small",
    icon_right: str = None,
    icon_right_size: str = "is-small",
    field_css_class: str = None,
    input_css_class: str = None,
    input_size: InputSizesStr = None,
    input_state: str = None,
    input_style: str = None,
    placeholder: str = None,
    control_css_class: str = None,
    field_template: str = "bulma/forms/fields.html",
):
    css_classes = {
        "label": css_class_string("sr-only" if inline else None),
        "field_label_size": css_class_string(f"is-{field_label_size}"),
        "field": css_class_string(field_css_class),
        "control": css_class_string(
            control_css_class,
            "has-icons-left" if icon_left else None,
            "has-icons-right" if icon_right else None,
        ),
        "input": css_class_string(
            input_css_class, input_size, input_state, input_style
        ),
        "icon_left": css_class_string(icon_left),
        "icon_left_size": css_class_string(f"is-{icon_left_size}"),
        "icon_right": css_class_string(icon_right),
        "icon_right_size": css_class_string(f"is-{icon_right_size}"),
    }

    widget_attrs = {
        "class": css_classes.get("input", ""),
    }
    if placeholder:
        widget_attrs.update({"placeholder": placeholder})

    context = {
        "field": field,
        "widget_attrs": widget_attrs,
        "css_classes": preprocess_markup_classes(css_classes, field),
        "form": field.form,
        "control_only": control_only,
        "is_horizontal": is_horizontal,
    }

    return get_template(field_template).render(context)


@register.simple_tag
def bulma_form(form, is_horizontal=False):
    has_management = getattr(form, "management_form", None)
    if has_management:
        template_name = "bulma/forms/formset.html"
        context = {
            "formset": form,
            "is_horizontal": is_horizontal,
        }
    else:
        template_name = "bulma/forms/form.html"
        context = {
            "form": form,
            "is_horizontal": is_horizontal,
        }

    return get_template(template_name).render(context)


@register.simple_tag
def font_awesome():
    """
    The latest FontAwesome CDN link.
    """
    cdn_link = (
        '<link rel="stylesheet" '
        'href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" '
        'integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" '
        'crossorigin="anonymous">'
    )
    return mark_safe(cdn_link)


def preprocess_markup_classes(markup_classes, bound_field):
    if any([is_file(bound_field), is_textarea(bound_field)]):
        markup_classes["control"] = markup_classes.get("control", "").replace(
            "has-icons-left", ""
        )
        markup_classes["control"] = markup_classes.get("control", "").replace(
            "has-icons-right", ""
        )
        markup_classes["control"] = markup_classes.get("control", "").strip()
    return markup_classes


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
    return isinstance(
        field.field.widget,
        (
            forms.TextInput,
            forms.NumberInput,
            forms.EmailInput,
            forms.PasswordInput,
            forms.URLInput,
        ),
    )


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


@register.simple_tag
def render_field_widget(field, attrs=None, css_class=None):
    if attrs is None:
        attrs = {}
    if not attrs.get("class"):
        attrs["class"] = ""
    if css_class:
        attrs["class"] += " " + css_class
    if len(field.errors) > 0:
        attrs["class"] += " is-danger"
    field_classes = field.field.widget.attrs.get("class", "")
    attrs["class"] += f" {field_classes}"
    return field.as_widget(attrs=attrs)


@register.filter
def bulma_message_tag(tag):
    return {"error": "danger"}.get(tag, tag)


@register.tag
def bulma_addons(parser, token):
    return _bulma_group_addons(parser, token, "endbulma_addons", "has-addons")


@register.tag
def bulma_group(parser, token):
    return _bulma_group_addons(parser, token, "endbulma_group", "is-grouped")


def _bulma_group_addons(parser, token, end_token, main_css_class):
    tag_name, arg = token.contents.split(None, 1)
    group_kwargs = {
        arg_val.split("=")[0]: arg_val.split("=")[1].lstrip('"').rstrip('"')
        for arg_val in arg.split(" ")
    }
    group_kwargs["css_class"] = f"{main_css_class} {group_kwargs.get('css_class')}"

    nodelist = parser.parse((end_token,))
    parser.delete_first_token()

    for node in nodelist:
        if isinstance(node, SimpleNode) and node.func in [bulma_field]:
            node.kwargs["wrap_with_field"] = FilterExpression("False", parser)
            node.kwargs["inline"] = FilterExpression("True", parser)

    return GroupNode(nodelist, group_kwargs)


class GroupNode(template.Node):
    def __init__(self, nodelist, group_kwargs):
        self.nodelist = nodelist
        self.group_kwargs = group_kwargs

    def render(self, context):
        output = self.nodelist.render(context)
        return f'<div class="field {self.group_kwargs.get("css_class")}">{output}</div>'


def tokens_to_dict(tokens):
    return {
        key_value[0]: key_value[1]
        for key_value in [token_to_tuple(token) for token in tokens.split(",")]
    }


def token_to_tuple(token):
    [name, value] = token.split("=")
    return strip_quotes(name), strip_quotes(value)


def strip_quotes(text):
    if not isinstance(text, str):
        return text
    if text.startswith('"'):
        text = text[1:]
    if text.endswith('"'):
        text = text[:-1]
    return text
