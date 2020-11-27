from django.shortcuts import render,redirect, get_object_or_404
from .models import * 
from .forms import * 
from django.contrib.auth.decorators import login_required
from datetime import datetime
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
 
def forumView(request):
    questions = Question.objects.all()
    context = {
        'questions': questions
    }
    return render(request,'discussionForum/index.html',context)

@login_required 
def addQuestion(request):
    if request.method == 'POST':
        form = CreateQuestionForm(request.POST)
        if form.is_valid():
            question = form.cleaned_data["question"]
            description = form.cleaned_data["description"]
            questionObject = Question.objects.create(createdBy=request.user,question=question,description=description)
            questionObject.save()
            print(questionObject)
            return redirect('forum')
    else:
        form = CreateQuestionForm()
    context ={'form':form}
    return render(request,'discussionForum/addQuestion.html',context)

@login_required
def updateQuestion(request,qid):
    if request.method == 'POST':
        form = UpdateQuestionForm(request.POST)
        if form.is_valid():
            question = get_object_or_404(Question,pk=qid)
            questionChanges = form.cleaned_data["question"]
            descriptionChanges = form.cleaned_data["description"]
            if questionChanges != "":
                question.question = questionChanges
            if descriptionChanges != "":
                question.description = descriptionChanges
            question.date_created = datetime.now()
            question.save()
            return redirect('forum')
    else:
        form = UpdateQuestionForm()
    context = {'form':form,'qid':qid}
    return render(request,'discussionForum/updateQuestion.html',context)

@login_required
def deleteQuestion(request,qid):
    question = get_object_or_404(Question,pk=qid)
    question.delete()
    return redirect('forum')

@login_required
def answerAQuestion(request,qid):
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            ans = form.cleaned_data["answer"]
            question = get_object_or_404(Question,pk=qid)
            answer = Answer.objects.create(question=question,answer=ans,answeredBy=request.user)
            answer.save()
            return redirect('forum')
    else:
        form = AnswerForm()
    context = {'form':form,'question':get_object_or_404(Question,pk=qid),'qid':qid}
    return render(request,"discussionForum/answerQuestion.html",context)

def viewAnswersOfQuestion(request,qid):
    question = get_object_or_404(Question,pk=qid)
    answers = question.answer_set.all()
    context = {'answers':answers}
    return render(request,"discussionForum/answers.html",context)      

@login_required
def updateAnswer(request,aid):
    if request.method == 'POST':
        form = UpdateAnswerForm(request.POST)
        if form.is_valid():
            ans = form.cleaned_data["answer"]
            answerObj = get_object_or_404(Answer,pk=aid)
            answerObj.answer = ans
            answerObj.date_answered = datetime.now()
            answerObj.save()
            qid = answerObj.question.id
            print(qid)
            return redirect('viewAnswers',qid=qid)
    else:
        form = UpdateAnswerForm()
    context = {'form':form,'aid':aid,"answer":get_object_or_404(Answer,pk=aid)}
    return render(request,"discussionForum/updateAnswer.html",context)

@login_required
def deleteAnswer(request,aid):
    answer = get_object_or_404(Answer,pk=aid)
    answer.delete()
    qid = answer.question.id
    print(qid)
    return redirect('viewAnswers',qid=qid)

@api_view(['GET'])
def questionAPIView(request):
    if request.method == 'GET':
        qs = Question.objects.all()
        serializer = QuestionSerializer(qs,many=True)
        print(serializer.data)
        print(Response(serializer.data))
        return Response(serializer.data)
    else:
        return redirect('forum')

@api_view(['GET'])
def answerAPIView(request):
    if request.method == 'GET':
        answerSet = Answer.objects.all()
        serializer = AnswerSerializer(answerSet,many=True)
        return Response(serializer.data)
    else:
        return redirect('forum')

@login_required
def upvoteAnswer(request,aid):
    answer = get_object_or_404(Answer,pk=aid)
    answer.votes += 1
    answer.save()
    return render(request,"discussionForum/answers.html",{"answers":Answer.objects.all()})

@login_required
def downvoteAnswer(request,aid):
    answer = get_object_or_404(Answer,pk=aid)
    answer.votes -= 1
    answer.save()
    return render(request,"discussionForum/answers.html",{"answers":Answer.objects.all()})

@login_required
def commentAnswer(request,aid):
    answer = get_object_or_404(Answer,pk=aid)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data["comment"]
            commentObject = Comment.objects.create(comment=comment,commentedBy=request.user,answer=answer)
            commentObject.save()
        return render(request,"discussionForum/answers.html",{"answers":Answer.objects.all()})
    else:
        form = CommentForm()
        context={"form":form,"answer":answer}
        return render(request,"discussionForum/comment.html",context)

        
    
