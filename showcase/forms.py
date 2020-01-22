from django import forms

COLOR_CHOICES = (
    ('red', 'Red'),
    ('green', 'Green'),
    ('blue', 'Blue')
)


class FormExample(forms.Form):
    text = forms.CharField()
    email = forms.EmailField()
    number = forms.CharField(widget=forms.NumberInput())
    url = forms.CharField(widget=forms.URLInput())
    password = forms.CharField(widget=forms.PasswordInput())
    select = forms.ChoiceField(choices=COLOR_CHOICES)
    multi_select = forms.MultipleChoiceField(choices=COLOR_CHOICES)
    textarea = forms.CharField(widget=forms.Textarea())
    checkbox = forms.BooleanField()
    checkboxes = forms.MultipleChoiceField(
        choices=COLOR_CHOICES,
        widget=forms.CheckboxSelectMultiple()
    )
    radios = forms.ChoiceField(
        choices=COLOR_CHOICES,
        widget=forms.RadioSelect()
    )
    file = forms.FileField(required=True)
