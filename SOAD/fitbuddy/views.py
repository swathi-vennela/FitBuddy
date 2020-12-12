from django.shortcuts import render,redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth import login,logout,authenticate
from django.views.generic import CreateView
from .models import User, Customer, FitnessCenter, Program, Review, HiringRole, EnrolledPrograms
from .forms import CustomerRegistrationForm,FitnessRegistrationForm, ProgramForm, ReviewForm, HiringRoleForm, CustomerProfileUpdateForm, FitnessCenterProfileUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from fitbuddy.decorators import *
from django.db.models import Q 
from django.db.models import Avg, Count
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
import stripe
stripe.api_key = "sk_test_51H0rNqD5fba9rsNuuXZqKUJlFtWrvxVLV7PkZZKMM8nwB7AXnEHHid6pCBWZFztSVUp40634OT2R9rkDCJCA0uJY00hSmmEOsF"
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import  DetailView
from . import models

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'fitbuddy/change_password.html', {
        'form': form
    })

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

# def register(request):
#     return render(request,'fitbuddy/register.html')

def view_programs(request):
    return render(request,'fitbuddy/program_list.html',context={'programs': Program.objects.all()})


def program_detail(request, slug):
    program = Program.objects.get(slug=slug)
    reviews = Review.objects.filter(program=program).order_by("-comment")
    average = reviews.aggregate(Avg("rating"))["rating__avg"]
    count = reviews.count()
    if average == None:
        average = 0
    average = round(average, 2)
    context = {
        "program" : program,
        'reviews' : reviews,
        "average": average,
        "count" : count
    }
    return render(request, 'fitbuddy/program_detail.html',context)

class customer_register(CreateView):
    model = User
    form_class = CustomerRegistrationForm
    template_name = 'fitbuddy/customer_register.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'customer'
        return super().get_context_data(**kwargs)
    def form_valid(self,form):
        user = form.save()
        login(self.request,user)
        return redirect('/')


class fitness_register(CreateView):
    model = User
    form_class = FitnessRegistrationForm
    template_name = 'fitbuddy/fitness_register.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'fitnesscenter'
        return super().get_context_data(**kwargs)
    def form_valid(self,form):
        user = form.save()
        login(self.request,user)
        return redirect('/')

## User Profile of Customer.
class CustomerDetailView(LoginRequiredMixin,DetailView):
    context_object_name = "customer"
    model = models.Customer
    template_name = 'fitbuddy/customer_detail_page.html'

## User Profile for Fitnesscenter.
class FitnesscenterDetailView(LoginRequiredMixin,DetailView):
    context_object_name = "fitnesscenter"
    model = models.FitnessCenter
    template_name = 'fitbuddy/fitnesscenter_detail_page.html'

## Profile update for students.
@login_required
def CustomerUpdateView(request,pk):
    profile_updated = False
    customer = get_object_or_404(models.Customer,pk=pk)
    if request.method == "POST":
        form = CustomerProfileUpdateForm(request.POST,instance=customer)
        if form.is_valid():
            profile = form.save(commit=False)
            if 'customer_profile_pic' in request.FILES:
                profile.customer_profile_pic = request.FILES['customer_profile_pic']
            profile.save()
            profile_updated = True
        return redirect('/')
    else:
        form = CustomerProfileUpdateForm(request.POST or None,instance=customer)
    return render(request,'fitbuddy/customer_update_page.html',{'profile_updated':profile_updated,'form':form})

## Profile update for teachers.
@login_required
def FitnessCenterUpdateView(request,pk):
    profile_updated = False
    fitnesscenter = get_object_or_404(models.FitnessCenter,pk=pk)
    if request.method == "POST":
        form = FitnessCenterProfileUpdateForm(request.POST,instance=fitnesscenter)
        if form.is_valid():
            profile = form.save(commit=False)
            if 'fitnesscenter_profile_pic' in request.FILES:
                profile.fitnesscenter_profile_pic = request.FILES['fitnesscenter_profile_pic']
            profile.save()
            profile_updated = True
        return redirect('/')
    else:
        form = FitnessCenterProfileUpdateForm(request.POST or None,instance=fitnesscenter)
    return render(request,'fitbuddy/fitnesscenter_update_page.html',{'profile_updated':profile_updated,'form':form})


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
def add_hiring_role(request,slug):
    program = Program.objects.get(slug = slug)
    if request.method == "POST" and request.user == program.fcenter.user:
        form = HiringRoleForm(request.POST, request.FILES)

        if form.is_valid():
            data = form.save(commit=False)
            data.contact_email = program.fcenter.email
            data.fprogram = program
            data.slug = datetime.now().strftime("%c")
            data.save()
            return redirect("program_detail",slug)
    else:
        form = HiringRoleForm()
    return render(request, 'fitbuddy/add_hiring_role.html',{"form":form})

def list_hiring_roles(request):
    return render(request, 'fitbuddy/hiring_list.html', context={'roles':HiringRole.objects.all()})

@api_view(http_method_names=['GET',])
def hiring_list_api_get(request):
    try:
        data = HiringRole.objects.all()
        serializer = HiringRoleSerializer(data,many=True)
        return Response(data=serializer.data)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


def job_detail(request, slug):
    job = HiringRole.objects.get(slug=slug)
    return render(request, 'fitbuddy/job_detail.html', context={'job':job})


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

def search_programs(request):
    query=request.GET.get('q1')
    if query:
        all_programs=Program.objects.all()
        results=all_programs.filter(Q(title__icontains=query)|Q(category__icontains=query))
    else:
        results=Program.objects.all()
    context={
        'programs' : results
    }
    return render(request,'fitbuddy/program_list.html',context)

def pricerange1(request):
	programs = Program.objects.filter(price__range=(0,1500))
	context={
		'programs' : programs
	}
	return render(request,'fitbuddy/program_list.html',context)	

def pricerange2(request):
	programs = Program.objects.filter(price__range=(1500,3000))
	context={
		'programs' : programs
	}
	return render(request,'fitbuddy/program_list.html',context)	

def pricerange3(request):
	programs = Program.objects.filter(price__range=(3000,5000))
	context={
		'programs' : programs
	}
	return render(request,'fitbuddy/program_list.html',context)	

def pricerange4(request):
	programs = Program.objects.filter(price__range=(5000,10000))
	context={
		'programs' : programs
	}
	return render(request,'fitbuddy/program_list.html',context)	

def add_review(request, slug):
    if request.user.is_authenticated:
        program = Program.objects.get(slug=slug)
        if request.method == "POST":
            form = ReviewForm(request.POST or None)
            if form.is_valid():
                data = form.save(commit=False)
                data.comment = request.POST["comment"]
                data.rating = request.POST["rating"]
                data.user = request.user
                data.program = program
                data.slug = datetime.now().strftime("%c")
                data.save()
                return redirect("program_detail", slug)
        else:
            form = ReviewForm()
        return render(request, 'fitbuddy/program_detail.html', {"form": form})
    else:
        return redirect("fitbuddy/login.html")

def edit_review(request, program_slug, review_slug):
    if request.user.is_authenticated:
        program = Program.objects.get(slug=program_slug)
        # review
        review = Review.objects.get(program=program, slug=review_slug)

        # check if the review was done by the logged in user
        if request.user == review.user:
            # grant permission
            if request.method == "POST":
                form = ReviewForm(request.POST, instance=review)
                if form.is_valid():
                    data = form.save(commit=False)
                    if (data.rating > 10) or (data.rating < 0):
                         error = "Out or range. Please select rating from 0 to 10."
                         return render(request, 'fitbuddy/edit_review.html', {"error": error, "form": form})
                    else:
                        data.save()
                        return redirect("program_detail", program_slug)
            else:
                form = ReviewForm(instance=review)
            return render(request, 'fitbuddy/edit_review.html', {"form": form})
        else:
            return redirect("program_detail", program_slug)
    else:
        return redirect("login")

def delete_review(request, program_slug, review_slug):
    if request.user.is_authenticated:
        program = Program.objects.get(slug=program_slug)
        # review
        review = Review.objects.get(program=program, slug=review_slug)

        # check if the review was done by the logged in user
        if request.user == review.user:
            # grant permission to delete
            review.delete()

        return redirect("program_detail", program_slug)
            
    else:
        return redirect("login")

@api_view(['GET'])
def programlist(request):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        programs = Program.objects.all()
    except programs.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer=ProgramSerializer(programs,serializer1,many=True)
        return Response(serializer.data)

@api_view(['GET'])
def programlistbyid(request,id):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        user=User.objects.get(id=id)
        fcenters=FitnessCenter.objects.get(user=user)
        programs=Program.objects.filter(fcenter=fcenters)
    except programs.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer=ProgramSerializer(programs,many=True)
        return Response(serializer.data)    

@api_view(['GET'])
def reviewlist(request,slug):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        programs=Program.objects.get(slug=slug)
        reviews=Review.objects.filter(program=programs)
    except reviews.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer=ReviewSerializer(reviews,many=True)
        return Response(serializer.data)    

def payment(request,slug):
	program = Program.objects.get(slug=slug)
	context = {'program':program}
	return render(request,'fitbuddy/payment.html',context)

def charge(request,slug):
    program = Program.objects.get(slug=slug)
    amount=program.price
    if request.method == 'POST':
        print('Data:', request.POST)
        customer = stripe.Customer.create(
            email=request.POST['email'],
            name=request.POST['name'],
            source=request.POST['stripeToken']
            )
        charge = stripe.Charge.create(
            customer=customer,
            amount=amount*100,
            currency='inr',
            description="Fitbuddy payment"
            )
        EnrolledPrograms.objects.create(program=program,username=request.user)
    return redirect(reverse('success'))

def successMsg(request):
	return render(request, 'fitbuddy/success.html')

def myenrolledprograms(request):
	programs = EnrolledPrograms.objects.filter(username=request.user)
	context={
		'programs' : programs
	}
	return render(request,'fitbuddy/my_programs.html',context)