from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from ckeditor.fields import RichTextField

# Create your models here.
class Autor(models.Model):

    class Meta:
        verbose_name_plural = 'Autores'
        verbose_name = 'Autor'
    
    nombre = models.CharField(max_length=100, null=True)
    avatar = models.ImageField(blank=True, null=True, upload_to="avatar")
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.nombre}'

class Media(models.Model):

    class Meta:
        verbose_name_plural = 'Media Files'
        verbose_name = 'Media'
        ordering = ["name"]
	
    image = models.ImageField(blank=True, null=True, upload_to="media")
    url = models.URLField(blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    is_image = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.url:
            self.is_image = False
        super(Media, self).save(*args, **kwargs)
    def __str__(self):
        return self.name

class Etiqueta(models.Model):
    class Meta:
       verbose_name_plural = 'Etiquetas'
       verbose_name = 'Etiqueta'
       ordering = ['nombre']
    
    nombre = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.nombre

class Blog(models.Model):

    class Meta:
        verbose_name_plural = 'Blogs'
        verbose_name = 'Blog'
        ordering = ["-fecha"]

    fecha = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, null=True)
    titulo = models.CharField(max_length=200, blank=True, null=True)
    descripcion = models.CharField(max_length=500, blank=True, null=True)
    contenido = RichTextField(blank=True, null=True)
    slug = models.SlugField(null=True, blank=True)
    imagen = models.ImageField(blank=True, null=True, upload_to="blog")
    etiquetas = models.ManyToManyField(Etiqueta, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.titulo)
        super(Blog, self).save(*args, **kwargs)

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return f"/blog/{self.slug}"

class Mangaka(models.Model):
    class Meta:
        verbose_name_plural = 'Mangakas'
        verbose_name = 'Mangaka'
        ordering = ['nombre']
    
    nombre = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.nombre

class Manga(models.Model):
    class Meta:
        verbose_name_plural = 'Mangas'
        verbose_name = 'Manga'
        ordering = ['nombre']
    
    nombre = models.CharField(max_length=200, null=True)
    mangaka = models.ForeignKey(Mangaka, on_delete=models.CASCADE)
    publicacion = models.DateField()
    volumenes = models.IntegerField(default=1)
    descripcion = models.CharField(max_length=500, blank=True, null=True)
    etiquetas = models.ManyToManyField(Etiqueta, blank=True)

    def __str__(self):
        return self.nombre

class Anime(models.Model):
    class Meta:
        verbose_name_plural = 'Animes'
        verbose_name = 'Anime'
        ordering = ['nombre']
    
    nombre = models.CharField(max_length=200, null=True)
    primera_emision = models.DateField()
    capitulos = models.IntegerField(default=1)
    duracion = models.DurationField(null=True)
    descripcion = models.CharField(max_length=500, blank=True, null=True)
    etiquetas = models.ManyToManyField(Etiqueta, blank=True)

    def __str__(self):
        return self.nombre