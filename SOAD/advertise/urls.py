from django.urls import include, path
from .views import *

urlpatterns = [
    path('fitness-product-list',fitnessproduct_list_view, name="fitness-product-list"),
    path('fitness-product/<slug:slug>',fitnessproduct_detail_view, name="fitnessproduct_detail"),
]