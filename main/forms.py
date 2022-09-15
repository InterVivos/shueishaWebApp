from django import forms
from ckeditor.fields import RichTextFormField
from .models import Anime, Blog, Manga, Review

class BlogCreateForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['autor', 'titulo', 'descripcion', 'contenido', 'imagen', 'etiquetas']

class CreateReview(forms.ModelForm):

    class Meta:
        model = Review
        fields = ('manga', 'anime', 'usuario', 'estrellas', 'mensaje')