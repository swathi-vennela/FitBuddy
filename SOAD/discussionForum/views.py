from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from .models import * 
from .forms import * 
# Create your views here.

def dummy(request):
    return render(request,'discussionForum/index.html')

def viewAnswers(request,topic):
    data = {
        'answers': []
    }
    for forum in Forum.objects.all():
        if forum.topic == topic:
            obj = forum
            break
    for answer in obj.discussion_set.all():
        data["answers"]+=answer.discuss
    return render(request,"discussionForum/answers.html",data)
 
def forumView(request):
    forums=Forum.objects.all()
    count=forums.count()
    discussions=[]
    for i in forums:
        discussions.append(i.discussion_set.all())
 
    context={'forums':forums,
              'count':count,
              'discussions':discussions}
    return render(request,'discussionForum/index.html',context)
 
def addForum(request):
    form = CreateInForum()
    if request.method == 'POST':
        form = CreateInForum(request.POST)
        if form.is_valid():
            form.save()
            return redirect('forum')
    context ={'form':form}
    return render(request,'discussionForum/addForum.html',context)
 
def addDiscussion(request,topic):
    form = CreateInDiscussion()
    if request.method == 'POST':
        form = CreateInDiscussion(request.POST)
        if form.is_valid():
            form.save()
            print(form)
            return redirect('forum')
    context ={'form':form,'forumName':topic}
    return render(request,'discussionForum/addDiscussion.html',context)