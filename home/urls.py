from home import views
from django.urls import path

urlpatterns = [
    path("", views.index_view, name="home"),
    path("gallery/", views.gallery_view, name="gallery"),
    ]