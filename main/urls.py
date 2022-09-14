from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .import views

app_name = 'main'

urlpatterns = [
    path('', views.IndexView.as_view(), name = "home"),
    path('blog/', views.BlogView.as_view(), name="blogs"),
    path('blog/<slug:slug>', views.BlogDetailView.as_view(), name="blog"),
    path('blog-create', views.blogcreate, name="blog-create"),
]