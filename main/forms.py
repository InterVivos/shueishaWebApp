from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Blog, Review

#Formularios

class BlogCreateForm(forms.ModelForm): #Formulario para crear blogs
    class Meta:
        model = Blog
        fields = ['autor', 'titulo', 'descripcion', 'contenido', 'imagen', 'etiquetas']
        widgets = {
            'descripcion': forms.Textarea(attrs={'cols':200, 'rows': 4,'style': "width: 70%;"}) #Mostrar el campo de descripción como un campo de texto multilínea
        }

class CreateReview(forms.ModelForm): #Formulario para crear reviews
    class Meta:
        model = Review
        fields = ['manga', 'anime', 'usuario', 'estrellas', 'mensaje']

class CreateUserForm(UserCreationForm): #Formulario para crear usuarios
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']