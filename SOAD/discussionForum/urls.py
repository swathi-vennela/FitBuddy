from django.contrib import admin
from django.urls import path
from discussionForum.views import *
 
urlpatterns = [
    path('',forumView,name='forum'),
    path('addQuestion/',addQuestion,name='addQuestion'),
    path('updateQuestion/<qid>',updateQuestion,name='updateQuestion'),
    path('deleteQuestion/<qid>',deleteQuestion,name='deleteQuestion'),
    path('answerAQuestion/<qid>',answerAQuestion,name='answerAQuestion'),
    path('viewAnswersOfQuestion/<qid>',viewAnswersOfQuestion,name='viewAnswers'),
    path('updateAnswer/<aid>',updateAnswer,name='updateAnswer'),
    path('deleteAnswer/<aid>',deleteAnswer,name='deleteAnswer'),
    # path('addDiscussion/<topic>',addDiscussion,name='answerForum'),
    # path('answers/<topic>',viewAnswers,name="viewAnswers"),
    # path('dummy/',dummy,name="dummy")
]