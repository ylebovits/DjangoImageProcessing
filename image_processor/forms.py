from django import forms
from image_processor.choices import FILTER_CHOICES


class UploadForm(forms.Form):
    imgFile = forms.FileField()
    filter = forms.ChoiceField(choices=FILTER_CHOICES)

