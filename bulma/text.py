# -*- coding: utf-8 -*-
from __future__ import unicode_literals


try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text


def text_value(value):
    """
    Force a value to text, render None as an empty string
    """
    if value is None:
        return ''
    return force_text(value)