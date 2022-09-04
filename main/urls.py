from django.urls import path
from .import views

app_name = 'main'

urlpatterns = [
    path('', views.IndexView.as_view(), name = "home"),
    path('blog/', views.BlogView.as_view(), name="blogs"),
    path('blog/<slug:slug>', views.BlogDetailView.as_view(), name="blog")
]