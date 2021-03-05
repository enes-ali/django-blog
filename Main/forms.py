from django import forms
from .models import *


class PostUploadForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ["title", "content", "cover_photo", "category"]
