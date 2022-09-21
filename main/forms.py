from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Blog, Review

class BlogCreateForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['autor', 'titulo', 'descripcion', 'contenido', 'imagen', 'etiquetas']
        widgets = {
            'descripcion': forms.Textarea(attrs={'cols':200, 'rows': 4,'style': "width: 70%;"})
        }

class CreateReview(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['manga', 'anime', 'usuario', 'estrellas', 'mensaje']

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']