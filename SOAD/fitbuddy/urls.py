from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

#app_name = 'fitbuddy'

urlpatterns=[
    path("", views.index_view, name='home'),

    # path('',views.index,name='index'),
    path('register/',views.register,name='register'),
    path('customer_register/',views.customer_register.as_view(),name='customer_register'),
    path('fitness_register/',views.fitness_register.as_view(),name='fitness_register'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('profile/', views.profile_view,name='profile'),
    path('add_program/',views.add_program, name='add_program'),
    path('list_programs/',views.view_programs, name='list_programs'),
    path('program_detail/<slug>', views.program_detail, name = 'program_detail'),
    path('edit_program/<slug>', views.edit_program, name='edit_program'),
    path('delete_program/<slug>', views.delete_program, name='delete_program'),
]