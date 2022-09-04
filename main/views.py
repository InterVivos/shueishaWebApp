from django.shortcuts import render
from django.contrib import messages
from .models import (
    UserProfile,
    Blog,
)
from django.views import generic
# Create your views here.

class IndexView(generic.TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blogs = Blog.objects.filter(is_active = True)
        
        context["blogs"] = blogs

        return context

class BlogView(generic.ListView):
    model = Blog
    template_name = "main/blog.html"
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(is_active = True)

class BlogDetailView(generic.DetailView):
    model = Blog
    template_name = "main/blog-detail.html"