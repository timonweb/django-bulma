import os
import shutil

import pytest

from bulma.tests.test_settings import STATICFILES_DIRS


@pytest.yield_fixture
def cleanup_static_files():
    static_files_dir = STATICFILES_DIRS[0]
    if os.path.isdir(static_files_dir):
        shutil.rmtree(static_files_dir)
    yield
    if os.path.isdir(static_files_dir):
        shutil.rmtree(static_files_dir)
