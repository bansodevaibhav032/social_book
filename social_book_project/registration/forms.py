from django import forms
from .models import UploadedFile
class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['title', 'file', 'description', 'visibility', 'cost', 'year_published']

class DisplayFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['title', 'description', 'visibility', 'cost', 'year_published']
        widgets = {'visibility': forms.HiddenInput()}
