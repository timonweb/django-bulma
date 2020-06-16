from ..utils import css_class_string


def test_css_class_string_returns_correct_classes():
    widget_name = 'text'

    assert css_class_string('control') == 'control'
    assert css_class_string(None) == ''
    assert css_class_string(False) == ''
    assert css_class_string(False, 'input', None) == 'input'

    assert css_class_string(
        'text-input' if widget_name == 'text' else None
    ) == 'text-input'

    assert css_class_string(
        'text-input' if widget_name == 'text' else None,
        'control'
    ) == 'text-input control'

    assert css_class_string(
        'number-input' if widget_name == 'number' else None,
        'control'
    ) == 'control'
