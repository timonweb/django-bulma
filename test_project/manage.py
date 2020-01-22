#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

    from django.core.management import execute_from_command_line
    from django.conf import settings
    settings.DEBUG = True

    execute_from_command_line(sys.argv)