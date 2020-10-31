from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns=[
    path('',views.index,name='index'),
    path('register/',views.register,name='register'),
    path('customer_register/',views.customer_register.as_view(),name='customer_register'),
    path('fitness_register/',views.fitness_register.as_view(),name='fitness_register'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
]