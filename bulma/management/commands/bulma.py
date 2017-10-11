import os
import subprocess
from django.conf import settings
from django.core.management import CommandError
from django.core.management.base import LabelCommand


class Command(LabelCommand):

    help = 'Runs bulma commands'
    missing_args_message = """
Command argument is missing, please add one of the following:
  install - to install npm packages necessary to build bulma sass
  build - to compile bulma sass into production css
  start - to start watching sass changes for dev
Usage example: 
  python manage.py bulma start
"""
    label = 'command'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.bulma_dir = os.path.join(settings.STATIC_ROOT, 'bulma', 'sass')

    def add_arguments(self, parser):
        parser.add_argument('args', metavar=self.label, help='Delete poll instead of closing it', nargs=1)

    def handle_label(self, label, **options):
        self.validate(label)
        getattr(self, 'handle_' + label)(**options)

    def validate(self, label):
        """
        Validates if STATIC_ROOT and bulma dir exist.
        """
        if not hasattr(settings, 'STATIC_ROOT'):
            raise CommandError("STATIC_ROOT isn't set in your settings. "
                               "Please set STATIC_ROOT before continue")

        if not os.path.exists(os.path.join(self.bulma_dir, 'package.json')):
            raise CommandError("It looks like you haven't copied bulma static files into your STATIC_ROOT yet. "
                           "Please run 'python manage.py copy_bulma_static_into_project' to copy bulma static files"
                           "and then comeback.")

        if label not in ['install', 'build', 'start']:
            raise CommandError("Subcommand doesn't exist")

    def handle_install(self, **options):
        self.npm_run(['install'])

    def handle_build(self, **options):
        self.npm_run(['run', 'build'])

    def handle_start(self, **options):
        self.npm_run(['run', 'start'])

    def npm_run(self, commands):
        try:
            subprocess.run(['npm'] + commands, cwd=self.bulma_dir)
        except KeyboardInterrupt:
            pass