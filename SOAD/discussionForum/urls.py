from django.contrib import admin
from django.urls import path
from discussionForum.views import *
 
urlpatterns = [
    path('',forumView,name='forum'),
    path('addForum/',addForum,name='addForum'),
    path('addDiscussion/<topic>',addDiscussion,name='answerForum'),
    path('answers/<topic>',viewAnswers,name="viewAnswers"),
    # path('dummy/',dummy,name="dummy")
]