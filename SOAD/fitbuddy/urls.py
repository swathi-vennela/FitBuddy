from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

#app_name = 'fitbuddy'

urlpatterns=[
    path("", views.index_view, name='home'),

    # path('',views.index,name='index'),
    # path('register/',views.register,name='register'),
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
    url(r'^results-programs/$',views.search_programs,name='search_programs'),
    path('pricerange1/',views.pricerange1,name='pricerange1'),
    path('pricerange2/',views.pricerange2,name='pricerange2'),
    path('pricerange3/',views.pricerange3,name='pricerange3'),
    path('pricerange4/',views.pricerange4,name='pricerange4'),
    path('addreview/<slug>', views.add_review, name="add_review"),
    path('editreview/<program_slug>/<review_slug>/', views.edit_review, name="edit_review"),
    path('deletereview/<program_slug>/<review_slug>/', views.delete_review, name="delete_review"),
    path('programs/',views.programlist,name='programs'),
    path('programs/<int:id>',views.programlistbyid,name='programs1'),
    path('add_hiring_role/<slug>',views.add_hiring_role, name='add_hiring_role'),
    path('list_hiring_roles/',views.list_hiring_roles, name='list_hiring_roles'),
    path('job_detail/<slug>/',views.job_detail, name='job_detail'),
    path('reviews/<slug>',views.reviewlist,name='reviews'),
    path('get_hiring_list/',views.hiring_list_api_get,name='get_hiring_list_api'),
    path('payment/<slug>/',views.payment,name='payment'),
    path('charge/<slug>/', views.charge, name="charge"),
    path('success', views.successMsg, name="success"),
    path('my_enrolled_programs/',views.myenrolledprograms,name='my_enrolled_programs')
]