from django import forms, template
from django.forms import BoundField
from django.template.base import FilterExpression
from django.template.library import SimpleNode
from django.template.loader import get_template
from django.utils.safestring import mark_safe

from bulma.utils import css_class_string

register = template.Library()
BULMA_COLUMN_COUNT = 1


@register.simple_tag
def bulma_label(field, template_name="bulma/forms/field_label.html"):
    return get_template(template_name).render({"field": field})


@register.simple_tag
def bulma_field(
    field,
    size=None,
    inline=False,
    control_only=False,
    is_horizontal=False,
    icon_left=None,
    icon_left_size=None,
    icon_right=None,
    icon_right_size=None,
    css_class=None,
    control_css_class=None,
    field_template=None,
):
    markup_classes = {
        "label": css_class_string("sr-only" if inline else None),
        "field": css_class_string(
            css_class, "is-horizontal" if is_horizontal else None
        ),
        "control": css_class_string(
            control_css_class,
            "has-icons-left" if icon_left else None,
            "has-icons-right" if icon_right else None,
        ),
        "input": css_class_string(size),
        "single_value": "",
        "icon_left": css_class_string(icon_left),
        "icon_left_size": css_class_string(
            f"is-{icon_left_size}" if icon_left_size else "is-small"
        ),
        "icon_right": css_class_string(icon_right),
        "icon_right_size": css_class_string(
            f"is-{icon_right_size}" if icon_right_size else "is-small"
        ),
    }
    return render_field(
        field,
        markup_classes=markup_classes,
        field_template=field_template,
        control_only=control_only,
        is_horizontal=is_horizontal,
    )


@register.simple_tag
def bulma_form(form):
    return render_form(form)


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


@register.filter(name="bulma")
def bulma_deprecated(element):
    markup_classes = {"label": "", "control": "", "single_value": ""}
    return legacy_render(element, markup_classes=markup_classes, control_only=False)


@register.filter(name="bulma_inline")
def bulma_inline_deprecated(element):
    markup_classes = {"label": "sr-only", "control": "", "single_value": ""}
    return legacy_render(element, markup_classes=markup_classes, control_only=False)


@register.filter(name="bulma_horizontal")
def bulma_horizontal_deprecated(element, label_cols="is-2"):
    markup_classes = {"label": label_cols, "control": "", "single_value": ""}

    for cl in label_cols.split(" "):
        splitted_class = cl.split("-")

        try:
            value_nb_cols = int(splitted_class[-1])
        except ValueError:
            value_nb_cols = BULMA_COLUMN_COUNT

        if value_nb_cols >= BULMA_COLUMN_COUNT:
            splitted_class[-1] = str(BULMA_COLUMN_COUNT)
        else:
            offset_class = cl.split("-")
            offset_class[-1] = "offset-" + str(value_nb_cols)
            splitted_class[-1] = str(BULMA_COLUMN_COUNT - value_nb_cols)
            markup_classes["single_value"] += " " + "-".join(offset_class)
            markup_classes["single_value"] += " " + "-".join(splitted_class)

        markup_classes["value"] += " " + "-".join(splitted_class)

    return legacy_render(element, markup_classes=markup_classes, control_only=False)


@register.filter
def add_input_classes(field, size=None):
    field_classes = field.field.widget.attrs.get("class", "")
    if len(field.errors) > 0:
        field_classes += " is-danger"
    if size:
        field_classes += " is-" + size
    field.field.widget.attrs["class"] = field_classes


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


def render_form(form, **kwargs):
    markup_classes = kwargs.pop("markup_classes", {})
    control_only = kwargs.pop("control_only", False)
    has_management = getattr(form, "management_form", None)
    if has_management:
        for formset_member in form.forms:
            for field in formset_member.visible_fields():
                add_input_classes(field)

        template_name = "bulma/forms/formset.html"
        context = {
            "formset": form,
            "classes": markup_classes,
            "control_only": control_only,
        }
    else:
        for field in form.visible_fields():
            add_input_classes(field)

        template_name = "bulma/forms/form.html"
        context = {
            "form": form,
            "classes": markup_classes,
            "control_only": control_only,
        }

    return get_template(template_name).render(context)


def render_field(field, **kwargs):
    context = {}
    markup_classes = kwargs.pop("markup_classes", {})
    template_name = kwargs.get("field_template") or "bulma/forms/fields.html"
    # if isinstance(field, BoundField):
    add_input_classes(field, markup_classes.get("input", ""))
    context.update(
        {
            "field": field,
            "classes": preprocess_markup_classes(markup_classes, field),
            "form": field.form,
            "control_only": kwargs.get("control_only", False),
            "is_horizontal": kwargs.get("is_horizontal", False),
        }
    )
    return get_template(template_name).render(context)


def legacy_render(element, **kwargs):
    markup_classes = kwargs.pop("markup_classes", {})
    wrap_with_field = kwargs.pop("wrap_with_field", True)

    template_name = kwargs.get("field_template") or "bulma/forms/fields.html"
    if isinstance(element, BoundField):
        add_input_classes(element, markup_classes.get("input", ""))
        context = {
            "field": element,
            "classes": preprocess_markup_classes(markup_classes, element),
            "form": element.form,
            "wrap_with_field": wrap_with_field,
        }
    else:
        has_management = getattr(element, "management_form", None)
        if has_management:
            for form in element.forms:
                for field in form.visible_fields():
                    add_input_classes(field)

            template_name = "bulma/forms/formset.html"
            context = {
                "formset": element,
                "classes": markup_classes,
                "wrap_with_field": wrap_with_field,
            }
        else:
            for field in element.visible_fields():
                add_input_classes(field)

            template_name = "bulma/forms/form.html"
            context = {
                "form": element,
                "classes": markup_classes,
                "wrap_with_field": wrap_with_field,
            }

    return get_template(template_name).render(context)


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


@register.filter
def addclass(field, css_class):
    if len(field.errors) > 0:
        css_class += " is-danger"
    field_classes = field.field.widget.attrs.get("class", "")
    field_classes += f" {css_class}"
    return field.as_widget(attrs={"class": field_classes})


@register.filter
def attrs(field, attrs):
    widget_attrs = field.field.widget.attrs or {}
    field.field.widget.attrs = {**widget_attrs, **tokens_to_dict(attrs)}
    return field


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
