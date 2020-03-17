from django import forms
from image_processor.choices import FILTER_CHOICES


class UploadForm(forms.Form):
    imgFile = forms.FileField(required=True)
    filter = forms.ChoiceField(choices=FILTER_CHOICES,
                               required=True)

