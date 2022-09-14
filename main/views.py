from urllib import request
from webbrowser import get
from django.shortcuts import render
from django.contrib import messages
from .models import (
    Blog
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

class BlogView(generic.ListView, RecentBlogs):
    model = Blog
    template_name = "main/blog.html"
    paginate_by = 3

    def get_queryset(self):
        return super().get_queryset().all()

class BlogDetailView(generic.DetailView, RecentBlogs):
    model = Blog
    template_name = "main/blog-detail.html"

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