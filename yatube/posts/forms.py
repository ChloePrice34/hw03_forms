from django import forms

from .models import Group, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        text = forms.CharField(required=True)
        group = forms.CharField(required=False)
        fields = ('text', 'group')