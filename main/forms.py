from django import forms
from ckeditor.fields import RichTextFormField
from .models import Blog

""" class ContactForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=True,
        widget = forms.TextInput(attrs={
            'placeholder': '*Full name...',
    }))
    email = forms.EmailField(max_length=254, required=True,
        widget = forms.TextInput(attrs={
            'placeholder': '*Email...',
    }))
    message = forms.CharField(max_length=1000, required=True,
        widget=forms.Textarea(attrs={
            'placeholder': '*Message...',
            'row': 6,
    }))

    class Meta:
        model = ContactProfile
        fields = ('name', 'email', 'message') """

class BlogCreateForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['autor', 'titulo', 'descripcion', 'contenido', 'imagen', 'etiquetas']