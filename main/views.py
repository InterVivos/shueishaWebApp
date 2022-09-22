from email import message
from typing_extensions import Self
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
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

# View de la página principal
class IndexView(generic.TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blogs = Blog.objects.all()[:6] #Tomar últimos 6 blogs y últimas 6 reviews
        reviews = Review.objects.all()[:6]
        
        context["blogs"] = blogs
        context["reviews"] = reviews #Anexar últimas reviews y blogs al contexto

        return context

# Clase base para obtener blogs recientes
class RecentBlogs(generic.base.ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recent_blogs = Blog.objects.all()[:4] # Tomar 4 últimos blogs
        context["recentBlogs"] = recent_blogs # Anexar al contexto

        return context

# Clase base para obtener y enviar reviews dependiendo si es anime o manga
class GetReviews(generic.edit.FormMixin):
    form_class = CreateReview
    formSent = None
    
    def get_success_url(self):
        return self.request.path # retornar a la misma página al procesar una solicitud sin errores

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = None
        if isinstance(self.object, Manga):
            reviews = Review.objects.filter(manga=self.object) #Si es manga, obtener las reviews para este
        else:
            reviews = Review.objects.filter(anime=self.object) #Si no, obtener las reviews para el anime
        
        context["form"] = CreateReview() #Anexar formulario para crear review, las reviews en sí
        context["reviews"] = reviews
        context["loop_n"] = range(5, 0, -1) # Y un iterador en reversa de 5 a 0 para la valoración en estrellas

        return context

    # al procesar una solicitud
    def post(self, request, *args, **kwargs):
        self.object = self.get_object() # obtener objeto de lasolicitud
        form = self.get_form() # obtener formulario enviado

        if form.is_valid(): #Si el formulario no contiene errores
            form1 = form.save(commit=False)
            if isinstance(self.object, Manga): #Determinar si la review es para un manga o un anime y anexar la llave foránea
                form1.manga = self.object
            else:
                form1.anime = self.object
            form1.save()
            return self.form_valid(form1) #Llamar al método de formulario exitoso
        else:
            return self.form_invalid(form)

    def form_valid(self, form): #Si todo fue bien con el formulario, llamar este método
        form.save()
        messages.success(self.request, "Reseña publicada exitosamente") #Enviar mensaje de solicitud correcta al usuario
        return super().form_valid(form)
    
    def form_invalid(self, form): #Si hubo un error con el formulario, llamar este método
        messages.error(self.request, "Error al publicar reseña") #Enviar mensaje de error al usuario
        return super().form_invalid(form)

#Subclase de RecentBlogs para mostrar la lista de blogs
class BlogView(generic.ListView, RecentBlogs):
    model = Blog
    template_name = "main/blog.html"
    paginate_by = 4 # Mostrar 4 por página

    def get_queryset(self):
        return super().get_queryset().all() #Tomar todos los blogs sin filtrar

#Clase para mostrar los detalles de un solo blog
class BlogDetailView(generic.DetailView, RecentBlogs):
    model = Blog
    template_name = "main/blog-detail.html"

#Clase para mostrar un listado de los mangas
class MangaView(generic.ListView):
    model = Manga
    template_name = "main/manga.html"
    paginate_by = 10 #Mostrar 10 por página

    def get_queryset(self):
        return super().get_queryset().all() # Tomar todos los mangas sin filtrar

#Clase para mostrar los detalles de un solo manga con sus reviews al heredar de GetReviews
class MangaDetailView(generic.DetailView, GetReviews):
    model = Manga
    template_name = "main/manga-detail.html"

#Clase para mostrar el listado de los animes
class AnimeView(generic.ListView):
    model = Anime
    template_name = "main/anime.html"
    paginate_by = 10 #Mostrar 10 por página

    def get_queryset(self):
        return super().get_queryset().all()

#Clase para mostrar los detalles de un solo anime con sus reviews al heredar de GetReviews
class AnimeDetailView(generic.DetailView, GetReviews):
    model = Anime
    template_name = "main/anime-detail.html"

#Vista de método para crear blogs (requiere inicio de sesión)
@login_required(login_url='/login')
def blogcreate(request):
    form = None
    if request.method == "POST": #Si estamos recibiendo una solicitud POST
        form = BlogCreateForm(request.POST, request.FILES) #Tomar solicitud POST con archivos
        if form.is_valid(): #Si la solicitud es correcta redireccionar a la misma página
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = BlogCreateForm() #Si no, anexar formulario al contexto
    return render(request, 'main/blog-create.html',{'form':form})

#Vista de método para manejar el registro e inicio de sesión
def loginRegister(request):
    if request.user.is_authenticated: #Si ya se inició sesión, devolver a la página principal
        return redirect('main:home')
    else:
        form = None
        if request.method == "POST": #Si no, tomamos la solicitud POST
            if 'password' in request.POST: #Si hay un campo llamado password, estamos lidiando con un inicio de sesión
                username = request.POST.get("username")
                password = request.POST.get("password")
                
                user = authenticate(request, username=username, password=password) #Intentar iniciar sesión con credenciales dadas

                if user is not None: #Si no obtuvimos un valor nulo, el inicio de sesión fue exitoso
                    login(request, user)
                    siguiente = request.GET.get('next')
                    if siguiente is None: return redirect('main:home') #Si el usuario no buscaba ir a otra página, redireccionarlo a la página principal
                    else: return redirect(siguiente)
                else:
                    messages.error(request, "Usuario o contraseña incorrecta")
            else:
                form = CreateUserForm(request.POST) #De otra manera, lidiamos con un registro
                if form.is_valid(): #Revisamos la validez del registro y si es válido creamos la cuenta
                    form.save()
                    user = form.cleaned_data.get('username')
                    messages.success(request, "Cuenta creada exitosamente, inicia sesión para acceder a la cuenta")

                    return redirect("main:login")
        context = {'form':form} #Anexar formulario al contexto
        return render(request, "main/login.html", context)
