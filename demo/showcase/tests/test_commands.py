from io import StringIO

from django.core.management import call_command


def test_copy_static_content():
    out = StringIO()
    call_command('copy_bulma_static_into_project', stdout=out)
    assert "Expected output" in out.getvalue()
