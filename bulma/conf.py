from django.conf import settings

BULMA_DEFAULTS = {
    "fontawesome_link": {
        "href": "https://use.fontawesome.com/releases/v5.7.2/css/all.css",
        "integrity": "sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr",
        "crossorigin": "anonymous",
    }
}


def get_bulma_setting(name, default=None):
    # Start with a copy of default settings
    BULMA = BULMA_DEFAULTS.copy()

    # Override with user settings from settings.py
    BULMA.update(getattr(settings, "BULMA_DEFAULTS", {}))

    return BULMA.get(name, default)
