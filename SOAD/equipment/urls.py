from django.urls import include, path
from .views import *

urlpatterns = [
    path('fitness-equipment-list',fitnessequipment_list_view, name="fitness-equipment-list"),
    path('fitness-equipment/<slug:slug>',fitnessequipment_detail_view, name="fitnessequipment_detail"),
]