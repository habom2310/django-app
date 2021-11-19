from django import forms
from .models import Content

class BlogForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = '__all__'

    file_upload = forms.FileField(label='Or select a file (.md)', required=False)
        

