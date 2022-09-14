from urllib import request
from webbrowser import get
from django.shortcuts import render
from django.contrib import messages
from .models import (
    Anime,
    Blog,
    Manga,
    Review
)
from .forms import BlogCreateForm
from django.http import HttpResponseRedirect
from django.views import generic
# Create your views here.

class IndexView(generic.TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blogs = Blog.objects.all()
        
        context["blogs"] = blogs

        return context

class RecentBlogs(generic.base.ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recent_blogs = Blog.objects.all()[:4]
        context["recentBlogs"] = recent_blogs

        return context

class GetReviews(generic.base.ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = None
        if isinstance(self.object, Manga): reviews = Review.objects.filter(manga=self.object)
        else: reviews = Review.objects.filter(anime=self.object)
        context["reviews"] = reviews
        context["loop_n"] = range(5, 0, -1)

        return context

class BlogView(generic.ListView, RecentBlogs):
    model = Blog
    template_name = "main/blog.html"
    paginate_by = 3

    def get_queryset(self):
        return super().get_queryset().all()

class BlogDetailView(generic.DetailView, RecentBlogs):
    model = Blog
    template_name = "main/blog-detail.html"

class MangaView(generic.ListView):
    model = Manga
    template_name = "main/manga.html"
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().all()

class MangaDetailView(generic.DetailView, GetReviews):
    model = Manga
    template_name = "main/manga-detail.html"

class AnimeView(generic.ListView):
    model = Anime
    template_name = "main/anime.html"
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().all()

class AnimeDetailView(generic.DetailView, GetReviews):
    model = Anime
    template_name = "main/anime-detail.html"

def blogcreate(request):
    form = None
    if request.method == "POST":
        form = BlogCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = BlogCreateForm()
    return render(request, 'main/blog-create.html',{'form':form})