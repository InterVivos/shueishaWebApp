from django.contrib import admin
from . models import (
    Autor,
    Media,
    Blog,
    Etiqueta,
    Mangaka,
    Manga,
    Anime,
    Review,
)
# Register your models here.
@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha')
    readonly_fields = ('slug',)

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Etiqueta)
class EtiquetaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')

@admin.register(Mangaka)
class MangakaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')

@admin.register(Manga)
class MangaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'mangaka')
    readonly_fields = ('slug',)

@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    readonly_fields = ('slug',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'fecha', 'manga', 'anime', 'estrellas')
