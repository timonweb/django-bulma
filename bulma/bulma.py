from django.conf import settings

BULMA_DEFAULTS = {
    # The URL to the jQuery JavaScript file
    # 'jquery_url': '//cdn.bootcss.com/jquery/1.12.4/jquery.min.js',

    # The Bulma base URL
    'base_url': '//cdn.bootcss.com/bulma/0.7.1/',

    # THE FontAwesome URL
    'font_awesome_url': "//cdn.bootcss.com/font-awesome/4.7.0/css/font-awesome.min.css",
}

# Start with a copy of default settings
BULMA = BULMA_DEFAULTS.copy()

BULMA.update(getattr(settings, 'BULMA', {}))


def get_bulma_setting(setting, default=None):
    """
    Read a setting
    """
    return BULMA.get(setting, default)


def bulma_url(postfix):
    """
    Prefix a relative url with the bootstrap base url
    """
    return get_bulma_setting('base_url') + postfix

#
# def jquery_url():
#     """
#     Return the full url to jQuery file to use
#     """
#     return get_bulma_setting('jquery_url')


def font_awesome_url():
    """
    Return the font-awesome file to use
    :return:
    """
    return get_bulma_setting('font_awesome_url')


def css_url():
    """
    Return the full url to the Bootstrap CSS file
    """
    url = get_bulma_setting('css_url')
    return url if url else bulma_url('css/bulma.min.css')
