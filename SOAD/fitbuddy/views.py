from django.shortcuts import render,redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth import login,logout,authenticate
from django.views.generic import CreateView
from .models import User, Customer, FitnessCenter, Program
from .forms import CustomerRegistrationForm,FitnessRegistrationForm, ProgramForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from fitbuddy.decorators import *

# Create your views here
def index_view(request):
    list={}
    fitcenter = FitnessCenter.objects.all()
    list["fitcenter"] = fitcenter
    context = {"fitcenter":fitcenter}
    return render(request, "fitbuddy/home.html",context=context)


@login_required
def profile_view(request):
    return render(request, "fitbuddy/profile.html")

# def index(request):
#     return render(request,'fitbuddy/index.html')

def register(request):
    return render(request,'fitbuddy/register.html')

def view_programs(request):
    return render(request,'fitbuddy/program_list.html',context={'programs': Program.objects.all()})

def program_detail(request, slug):
    program = Program.objects.get(slug=slug)
    context = {
        "program" : program,
    }
    return render(request, 'fitbuddy/program_detail.html',context)

class customer_register(CreateView):
    model = User
    form_class = CustomerRegistrationForm
    template_name = 'fitbuddy/customer_register.html'

    def form_valid(self,form):
        user = form.save()
        login(self.request,user)
        return redirect('/')


class fitness_register(CreateView):
    model = User
    form_class = FitnessRegistrationForm
    template_name = 'fitbuddy/fitness_register.html'

    def form_valid(self,form):
        user = form.save()
        login(self.request,user)
        return redirect('/')

def login_view(request):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('/')
            else:
                messages.error(request,"Invalid username or password")
        else:
                messages.error(request,"Invalid username or password")

    return render(request,'fitbuddy/login.html',context={'form':AuthenticationForm()})

def logout_view(request):
    logout(request)
    return redirect('/')

@fitness_center_required
def add_program(request):
    if request.method == "POST":
        form = ProgramForm(request.POST, request.FILES)

        if form.is_valid():
            data = form.save(commit=False)
            fcenter = FitnessCenter.objects.get(user=request.user)
            data.fcenter = fcenter
            data.slug = datetime.now().strftime("%c")
            data.save()
            return redirect('/')

    else:
        form = ProgramForm()
    return render(request, 'fitbuddy/add_program.html',{"form":form})

@fitness_center_required
def edit_program(request, slug):    
	program = Program.objects.get(slug=slug)
	if request.method == "POST" and request.user == program.fcenter.user:
		form = ProgramForm(request.POST, instance=program)
		if form.is_valid():
				data = form.save(commit=False)
				data.save()
				return redirect("program_detail", slug)
	else:
		form = ProgramForm(instance=program)
	return render(request, 'fitbuddy/add_program.html', {"form": form})

@fitness_center_required
def delete_program(request, slug):
    context = {}
    program = get_object_or_404(Program, slug=slug)
    if request.method == "POST" and request.user == program.fcenter.user :
        program.delete()
        return redirect("list_programs")
    return render(request, 'fitbuddy/program_delete.html',context)

