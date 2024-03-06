from django import forms
from .models import UploadedFile
class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['title', 'file', 'description','cover_photo','visibility', 'cost', 'year_published']

class DisplayFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['title', 'description', 'cover_photo','visibility', 'cost', 'year_published']
        widgets = {'visibility': forms.HiddenInput()}
