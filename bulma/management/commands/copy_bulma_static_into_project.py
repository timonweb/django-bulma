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
        self.storage = staticfiles_storage
        self.is_filesystem_storage = issubclass(staticfiles_storage.__class__, FileSystemStorage)

    def handle(self, *args, **options):
        self.validate()
        self.clear_dir('bulma')
        self.copy_bulma_files()

    def validate(self):
        """
        Validates if STATIC_ROOT exists and if bulma dir exists.
        """
        if not hasattr(settings, 'STATIC_ROOT'):
            raise CommandError("STATIC_ROOT isn't set in your settings. "
                               "Please set STATIC_ROOT before continue")

        if self.storage.exists('bulma'):
            result = input("'bulma' dir already exists in your STATIC_ROOT, "
                           "do you want to overwrite its contents and continue? y/N: ")
            if result.lower() != 'y':
                raise CommandError('Command aborted')

    def clear_dir(self, path):
        """
        Deletes the given relative path using the destination storage backend.
        """
        dirs, files = self.storage.listdir(path)

        for f in files:
            fpath = os.path.join(path, f)
            try:
                full_path = self.storage.path(fpath)
            except NotImplementedError:
                self.storage.delete(fpath)
            else:
                if not os.path.exists(full_path) and os.path.lexists(full_path):
                    # Delete broken symlinks
                    os.unlink(full_path)
                else:
                    self.storage.delete(fpath)
        for d in dirs:
            if self.is_filesystem_storage:
                shutil.rmtree(os.path.join(settings.STATIC_ROOT, path, d))
            else:
                self.clear_dir(os.path.join(path, d))

    def copy_bulma_files(self):
        """
        Copies Bulma static files from package's static/bulma into project's
        STATIC_ROOT/bulma
        """
        root = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'static',
            'bulma'
        )
        for path, _, files in os.walk(root):
            for name in files:
                with open(os.path.join(path, name)) as source_file:
                    dirname = os.path.relpath(path, root)
                    self.storage.save(name=os.path.join('bulma', dirname, name), content=source_file)
