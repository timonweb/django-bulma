try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

try:
    from urlparse import urlparse, parse_qs, urlunparse
except ImportError:
    from urllib.parse import urlparse, parse_qs, urlunparse

from django.forms.utils import flatatt
from django.utils.encoding import force_str, force_text
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


def url_replace_param(url, name, value):
    """
    Replace a GET parameter in an URL
    """
    url_components = urlparse(force_str(url))
    query_params = parse_qs(url_components.query)
    query_params[name] = value
    query = urlencode(query_params, doseq=True)
    return force_text(urlunparse([
        url_components.scheme,
        url_components.netloc,
        url_components.path,
        url_components.params,
        query,
        url_components.fragment,
    ]))
