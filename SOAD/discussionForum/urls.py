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
    path('api/questions',questionAPIView,name='apiQuestions'),
    path('api/answers',answerAPIView,name='apiAnswers'),
    path('answer/<aid>/upvote',upvoteAnswer,name='upvote'),
    path('answer/<aid>/downvote',downvoteAnswer,name='downvote'),
    path('answer/<aid>/comment',commentAnswer,name='comment'),
    path('recentQuestions/',recentQuestions,name='recentQuestions'),
    path('api/questions/recent',recentQuestionsAPIView,name='recentQuestionsAPI'),
    path('sortAnswersByVotes/<qid>',sortAnswersByVotes,name='sortAnswersByVotes'),
    path('api/answers/sortedVotes/<qid>',sortAnswersByVotesAPIView,name='sortAnswersByVotesAPI'),
    path('answers/recent/<qid>',recentAnswers,name='recentAnswers'),
    path('api/answers/recent/<qid>',recentAnswersAPIView,name='recentAnswersAPI'),
]