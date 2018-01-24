# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from importlib import import_module

from django import VERSION as DJANGO_VERSION
from django.conf import settings


# Do we support set_required and set_disabled?
# See GitHub issues 337 and 345
# TODO: Get rid of this after support for Django 1.8 LTS ends
DBS3_SET_REQUIRED_SET_DISABLED = DJANGO_VERSION[0] < 2 and DJANGO_VERSION[1] < 10


BULMA_DEFAULTS = {
    # The URL to the jQuery JavaScript file
    'jquery_url': '//cdn.bootcss.com/jquery/1.12.4/jquery.min.js',

    # The Bootstrap base URL
    'base_url': '//cdn.bootcss.com/bulma/0.6.2/',
}


# Start with a copy of default settings
BULMA = BULMA_DEFAULTS.copy()


BULMA.update(getattr(settings, 'BULMA', {}))