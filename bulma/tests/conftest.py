import os
import pytest
import shutil
from django.conf import settings


@pytest.yield_fixture
def cleanup_static_files():
    static_files_dir = settings.STATICFILES_DIRS[0]
    if os.path.isdir(static_files_dir):
        shutil.rmtree(static_files_dir)
    yield
    if os.path.isdir(static_files_dir):
        shutil.rmtree(static_files_dir)
