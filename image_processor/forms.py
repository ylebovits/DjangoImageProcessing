from django import forms
from image_processor.choices import FILTER_CHOICES
from .validators import image_validator


class UploadForm(forms.Form):
    imgFile = forms.FileField(required=True,
                              validators=[image_validator])

    filter = forms.ChoiceField(choices=FILTER_CHOICES,
                               required=True)

