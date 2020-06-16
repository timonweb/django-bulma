import pytest
from django import forms

from .utils import render_form, get_dom, assert_element_has_all_attributes

COLOR_CHOICES = (
    ('red', 'Red'),
    ('green', 'Green'),
    ('blue', 'Blue')
)


@pytest.mark.parametrize("field,label,tag,attributes", [
    (forms.CharField(), "Name", 'input', {
        'name': 'name',
        'class': ['input'],
        'type': 'text'
    }),
    (forms.EmailField(), "Email", 'input', {
        'name': 'email',
        'class': ['input'],
        'type': 'email'
    }),
    (forms.CharField(widget=forms.NumberInput()), "Age", 'input', {
        'name': 'age',
        'class': ['input'],
        'type': 'number'
    }),
    (forms.CharField(widget=forms.URLInput()), "Url", 'input', {
        'name': 'url',
        'class': ['input'],
        'type': 'url'
    }),
    (forms.CharField(widget=forms.PasswordInput()), "Password", 'input', {
        'name': 'password',
        'class': ['input'],
        'type': 'password'
    }),
    (forms.ChoiceField(choices=[]), "Select", 'select', {
        'name': 'choice'
    }),
    (forms.MultipleChoiceField(choices=[]), "Multi select", 'select', {
        'name': 'multichoice',
        'multiple': ""
    }),
    (forms.CharField(widget=forms.Textarea()), "Textarea", 'textarea', {
        'name': 'text',
        'class': ['textarea']
    }),
    (forms.BooleanField(), "Checkbox", 'input', {
        'name': 'agree',
        'type': 'checkbox'
    }),
    (forms.MultipleChoiceField(
        choices=COLOR_CHOICES,
        widget=forms.CheckboxSelectMultiple()
    ), "Checkboxes", 'input', {
         'name': 'items',
         'type': 'checkbox',
         'value': 'red'
     }),
    (forms.ChoiceField(
        choices=COLOR_CHOICES,
        widget=forms.RadioSelect()
    ), "Radios", 'input', {
         'name': 'choice',
         'type': 'radio',
         'value': 'red'
     }),
    (forms.FileField(), "File input", 'input', {
        'name': 'upload',
        'type': 'file',
        'class': ['file-input']
    })
])
def test_input_rendering(field, tag, label, attributes):

    class TestForm(forms.Form):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields[attributes['name']] = field
            self.fields[attributes['name']].label = label

    output = render_form(TestForm())
    dom = get_dom(output)

    assert_element_has_all_attributes(dom.find(tag), attributes), f"{label} has attributes {str(attributes)}"
    assert dom.find('label').text.strip() == label, f"Field has label {label}"
