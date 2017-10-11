import os
import shutil
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.management import BaseCommand, CommandError
from django.contrib.staticfiles.storage import staticfiles_storage


class Command(BaseCommand):
    help = 'Copies bulma static files into project\'s main static dir'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.static_root_bulma_dir = os.path.join(settings.STATIC_ROOT, 'bulma')

    def handle(self, *args, **options):
        self.validate()
        self.copy_bulma_files()

    def validate(self):
        """
        Validates if STATIC_ROOT exists and if bulma dir exists.
        """
        if not hasattr(settings, 'STATIC_ROOT'):
            raise CommandError("STATIC_ROOT isn't set in your settings. "
                               "Please set STATIC_ROOT before continue")

        if os.path.exists(self.static_root_bulma_dir):
            result = input("'bulma' dir already exists in your STATIC_ROOT, "
                           "do you want to overwrite its contents and continue? y/N: ")
            if result.lower() != 'y':
                raise CommandError('Command aborted')
            shutil.rmtree(self.static_root_bulma_dir)

    def copy_bulma_files(self):
        """
        Copies Bulma static files from package's static/bulma into project's
        STATIC_ROOT/bulma
        """
        original_bulma_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'static',
            'bulma'
        )
        shutil.copytree(original_bulma_dir, self.static_root_bulma_dir)
