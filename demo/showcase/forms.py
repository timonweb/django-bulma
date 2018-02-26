from django import forms

COLOR_CHOICES = (
    ('red', 'Red'),
    ('green', 'Green'),
    ('blue', 'Blue')
)


class FormExample(forms.Form):
    text = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    number = forms.CharField(required=False, widget=forms.NumberInput())
    url = forms.CharField(required=False, widget=forms.URLInput())
    password = forms.CharField(required=False, widget=forms.PasswordInput())
    select = forms.ChoiceField(required=False, choices=COLOR_CHOICES)
    multi_select = forms.MultipleChoiceField(required=False, choices=COLOR_CHOICES)
    textarea = forms.CharField(required=False, widget=forms.Textarea())
    checkbox = forms.BooleanField(required=False)
    checkboxes = forms.MultipleChoiceField(
        required=False,
        choices=COLOR_CHOICES,
        widget=forms.CheckboxSelectMultiple()
    )
    radios = forms.ChoiceField(
        required=False,
        choices=COLOR_CHOICES,
        widget=forms.RadioSelect()
    )
    file = forms.FileField(required=True)
