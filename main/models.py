from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

#Modelos de las clases en la base de datos

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
        ordering = ["name"] #ordenar archivos multimedia por nombre
	
    image = models.ImageField(blank=True, null=True, upload_to="media")
    url = models.URLField(blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    is_image = models.BooleanField(default=True)

    def save(self, *args, **kwargs): #Al guardar, revisar si es una imagen o la dirección a una
        if self.url:
            self.is_image = False
        super(Media, self).save(*args, **kwargs)
    def __str__(self):
        return self.name

class Etiqueta(models.Model):
    class Meta:
       verbose_name_plural = 'Etiquetas'
       verbose_name = 'Etiqueta'
       ordering = ['nombre'] #ordenar etiquetas por nombre
    
    nombre = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.nombre

class Blog(models.Model):

    class Meta:
        verbose_name_plural = 'Blogs'
        verbose_name = 'Blog'
        ordering = ["-fecha"] #ordenar blogs por fecha

    fecha = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, null=True)
    titulo = models.CharField(max_length=200, blank=True, null=True)
    descripcion = models.CharField(max_length=500, blank=True, null=True)
    contenido = RichTextUploadingField(blank=True, null=True)
    slug = models.SlugField(null=True, blank=True)
    imagen = models.ImageField(blank=True, null=True, upload_to="blog")
    etiquetas = models.ManyToManyField(Etiqueta, blank=True)

    def save(self, *args, **kwargs): #Al guardar, crear el slug a partir del título del blog
        if not self.id:
            self.slug = slugify(self.titulo)
        super(Blog, self).save(*args, **kwargs)

    def __str__(self):
        return self.titulo

    def get_absolute_url(self): #Método para obtener el url del objeto blog con su slug
        return f"/blog/{self.slug}"

class Mangaka(models.Model):
    class Meta:
        verbose_name_plural = 'Mangakas'
        verbose_name = 'Mangaka'
        ordering = ['nombre'] #Ordenar mangakas por nombre
    
    nombre = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.nombre

class Manga(models.Model):
    class Meta:
        verbose_name_plural = 'Mangas'
        verbose_name = 'Manga'
        ordering = ['nombre'] #Ordenar mangas por nombre
    
    nombre = models.CharField(max_length=200, null=True)
    mangaka = models.ForeignKey(Mangaka, on_delete=models.CASCADE)
    publicacion = models.DateField()
    volumenes = models.IntegerField(default=1)
    descripcion = models.CharField(max_length=500, blank=True, null=True)
    imagen = models.ImageField(blank=True, null=True, upload_to="manga")
    etiquetas = models.ManyToManyField(Etiqueta, blank=True)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs): #Al guardar, crear un slug a partir del nombre del manga
        if not self.id:
            self.slug = slugify(self.nombre)
        super(Manga, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/manga/{self.slug}" #Método para obtener el url del objeto manga con su slug

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
    imagen = models.ImageField(blank=True, null=True, upload_to="anime")
    etiquetas = models.ManyToManyField(Etiqueta, blank=True)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs): #Al guardar, crear un slug a partir del nombre del anime
        if not self.id:
            self.slug = slugify(self.nombre)
        super(Anime, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/anime/{self.slug}" #Método para obtener el url del objeto anime con su slug

class Review(models.Model):
    class Meta:
        verbose_name_plural = 'Reviews'
        verbose_name = 'Review'
        ordering = ['-fecha'] #ordenar reviews por fecha
        """ constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_anime_or_manga",
                check=(
                    models.Q(manga__isnull=True, anime__isnull=False)
                    | models.Q(manga__isnull=False, anime__isnull=True)
                ),
            )
        ] """
    
    opciones_calif = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')] #Restringir la valoración de 1 a 5
    
    usuario = models.CharField(max_length=100, null=True)
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE, blank=True, null=True, default=None)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, blank=True, null=True, default=None)
    fecha = models.DateTimeField(auto_now_add=True)
    estrellas = models.PositiveIntegerField(default=1, null=True, choices=opciones_calif)
    mensaje = models.CharField(max_length=500, null=True)