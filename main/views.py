from email import message
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from .models import (
    Anime,
    Blog,
    Manga,
    Review
)
from .forms import BlogCreateForm, CreateReview, CreateUserForm
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

class GetReviews(generic.edit.FormMixin):
    form_class = CreateReview
    formSent = None
    
    def get_success_url(self):
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = None
        if isinstance(self.object, Manga):
            reviews = Review.objects.filter(manga=self.object)
        else:
            reviews = Review.objects.filter(anime=self.object)
        
        context["form"] = CreateReview()
        context["reviews"] = reviews
        context["loop_n"] = range(5, 0, -1)

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            form1 = form.save(commit=False)
            if isinstance(self.object, Manga):
                form1.manga = self.object
            else:
                form1.anime = self.object
            form1.save()
            return self.form_valid(form1)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Reseña publicada exitosamente")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Error al publicar reseña")
        return super().form_invalid(form)

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

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('main:home')
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, "Account created")

                return redirect("main:login")
        context = {'form':form}
        return render(request, 'main/register.html', context)

def login1(request):
    if request.user.is_authenticated:
        return redirect('main:home')
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("main:home")
            else:
                message.error(request, "Usuario o contraseña incorrecta")

        context = {}
        return render(request, "main/login.html", context)

def loginRegister(request):
    if request.user.is_authenticated:
        return redirect('main:home')
    else:
        form = None
        if request.method == "POST":
            if 'password' in request.POST:
                print("login in")
                username = request.POST.get("username")
                password = request.POST.get("password")
                
                user = authenticate(request, username=username, password=password)

                if user is not None:
                    login(request, user)
                    return redirect("main:home")
                else:
                    messages.error(request, "Usuario o contraseña incorrecta")
            else:
                print("login out")
                form = CreateUserForm(request.POST)
                if form.is_valid():
                    form.save()
                    user = form.cleaned_data.get('username')
                    messages.success(request, "Account created")

                    return redirect("main:login")
        context = {'form':form}
        return render(request, "main/login.html", context)
