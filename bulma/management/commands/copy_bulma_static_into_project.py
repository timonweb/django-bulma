import os
import shutil
from django.conf import settings
from django.core.management import BaseCommand, CommandError


class Command(BaseCommand):

    help = 'Copies bulma static files into project\'s main static dir'
    static_root_bulma_dir = None

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        self.validate()
        self.copy_bulma_files()

    def validate(self):

        if len(settings.STATICFILES_DIRS) == 0:
            raise CommandError(
                "STATICFILES_DIRS in your settings is empty. "
                "STATICFILES_DIRS should have at least one directory. "
                "Bulma static files will be put into first directory listed in STATICFILES_DIRS "
                "It's a good idea to set first item of STATICFILES_DIRS to os.path.join(BASE_DIR, \"static\")"
            )

        self.static_root_bulma_dir = os.path.join(settings.STATICFILES_DIRS[0], 'bulma')

        if os.path.exists(self.static_root_bulma_dir):
            result = input("'bulma' dir already exists in your first STATICFILES_DIRS directory, "
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