import os
import subprocess
from django.conf import settings
from django.core.management import CommandError
from django.core.management.base import LabelCommand


class Command(LabelCommand):
    help = 'Runs bulma npm commands'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.bulma_dir = os.path.join(settings.STATIC_ROOT, 'bulma', 'sass')

    def handle(self, *args, **options):
        self.validate()
        try:
            subprocess.run(['npm'] + list(args), cwd=self.bulma_dir)
        except KeyboardInterrupt:
            pass

    def validate(self):
        """
        Validates if STATIC_ROOT exists and if bulma dir exists.
        """
        if not hasattr(settings, 'STATIC_ROOT'):
            raise CommandError("STATIC_ROOT isn't set in your settings. "
                               "Please set STATIC_ROOT before continue")

        if not os.path.exists(os.path.join(self.bulma_dir, 'package.json')):
            raise CommandError("It looks like you haven't copied bulma static files into your STATIC_ROOT yet. "
                           "Please run python manage.py copy_bulma_static_into_project to copy bulma static files"
                           "and then comeback.")