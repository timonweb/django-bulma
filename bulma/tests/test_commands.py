import os
from io import StringIO

import pytest
from django.core.management import call_command, CommandError

from django.conf import settings

BULMA_STATIC_DIR = os.path.join(settings.STATICFILES_DIRS[0], 'bulma')


def test_bulma_command_without_second_argument_displays_command_error_message():
    out = StringIO()
    with pytest.raises(CommandError) as err:
        call_command('bulma', stdout=out)

    assert 'Command argument is missing, please add one of the following' in str(err.value)


def test_copy_static_content(cleanup_static_files):
    style_css = os.path.join(BULMA_STATIC_DIR, 'css', 'style.css')
    style_sass = os.path.join(BULMA_STATIC_DIR, 'sass', 'style.sass')
    package_json = os.path.join(BULMA_STATIC_DIR, 'sass', 'package.json')

    out = StringIO()
    call_command('copy_bulma_static_into_project', stdout=out)

    assert os.path.isfile(style_css), f'{str(style_css)} has been created'
    assert os.path.isfile(style_sass), f'{str(style_sass)} has been created'
    assert os.path.isfile(package_json), f'{str(package_json)} has been created'


def test_bulma_install_command(cleanup_static_files):
    call_command('copy_bulma_static_into_project')

    out = StringIO()
    call_command('bulma', 'install', stdout=out)

    assert os.path.isdir(os.path.join(BULMA_STATIC_DIR, 'sass', 'node_modules')), "node_modules have been created"
    assert os.path.isfile(
        os.path.join(BULMA_STATIC_DIR, 'sass', 'package-lock.json')), "package-lock.json has been created"


def test_bulma_build_command(cleanup_static_files):
    style_css = os.path.join(BULMA_STATIC_DIR, 'css', 'style.css')
    style_min_css = os.path.join(BULMA_STATIC_DIR, 'css', 'style.min.css')

    call_command('copy_bulma_static_into_project')

    # Delete preinstalled files
    os.remove(style_css)
    os.remove(style_min_css)

    call_command('bulma', 'install')

    out = StringIO()
    call_command('bulma', 'build', stdout=out)

    # Ensure new file have been generated
    assert os.path.isfile(style_css), f'{str(style_css)} has been created'
    assert os.path.isfile(style_min_css), f'{str(style_min_css)} has been created'
