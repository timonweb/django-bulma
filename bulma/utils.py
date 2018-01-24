from django.utils.safestring import mark_safe
from django.utils.html import format_html

from .text import text_value


def render_link_tag(url, rel='stylesheet', media=None):
    """
    Build a link tag
    """
    attrs = {
        'href': url,
        'rel': rel,
    }
    if media:
        attrs['media'] = media
    return render_tag('link', attrs=attrs, close=False)

def render_tag(tag, attrs=None, content=None, close=True):
    """
    Render a HTML tag
    """
    builder = '<{tag}{attrs}>{content}'
    if content or close:
        builder += '</{tag}>'
    return format_html(
        builder,
        tag=tag,
        attrs=mark_safe(flatatt(attrs)) if attrs else '',
        content=text_value(content),
    )