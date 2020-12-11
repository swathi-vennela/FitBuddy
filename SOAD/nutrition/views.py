from django.shortcuts import render, redirect
from .forms import NutritionExtractionForm
from django.contrib.auth.decorators import login_required
import requests
from decimal import *
from django.http import JsonResponse
from .models import *

def getExpectedEnergyRequirement(activity,age,height,weight,gender):
    if activity == "sedentary":
        physicalActivityLevel = 1.00
    elif activity == "low active":
        physicalActivityLevel = 1.40
    elif activity == "active":
        physicalActivityLevel = 1.60
    else:
        physicalActivityLevel = 1.90
    if gender == "female":
        if age < 19:
            result = 135.30 - (30.80 * age) + physicalActivityLevel * ((10.0 * weight) + (934 * height)) + 25
        else:
            result = 354 - (6.91 * age) + physicalActivityLevel * ((9.36 * weight) + (726 * height))
    else:
        if age < 19:
            result = 88.5 - (61.9 * age) + physicalActivityLevel * ((26.7 * weight) + (903 * height)) + 25
        else:
            result = 662 - (9.53 * age) + physicalActivityLevel * ((15.91 * weight) + (539.6 * height))
    return result

    # pass

def getNutrition(json):
    app_id = "e7ce2d76"
    key = "bae49c1ce6113d57e30264f172f97484"
    url = "https://api.edamam.com/api/nutrition-details"
    payload = {
        "app_id": app_id,
        "app_key": key
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url,params=payload,json=json,headers=headers)
    return response.json()

@login_required
def nutritionAnalyzer(request):
    context = {
        'form': None,
        'data': None
    }
    if request.method == "POST":
        form = NutritionExtractionForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            ingredients = form.cleaned_data["ingredients"]
            items = []
            items = ingredients.splitlines()
            json = {
                "title": title,
                "ingr": items
            }
            data = getNutrition(json)
            context["data"] = data
            calories = data["calories"]
            caloriesObject = Calorie.objects.create(nutrition=request.user.customer.nutritionofcustomer,calories=calories)
            caloriesObject.save()
            # request.user.customer.nutritionofcustomer.caloriesIntake = calories
            # request.user.customer.nutritionofcustomer.save()
            # print(request.user.customer.nutritionofcustomer.caloriesIntake)
        else:
            print(form.errors)
    else:
        form = NutritionExtractionForm()
    context["form"] = form
    return render(request,"nutrition/nutritionAnalysis.html",context)

@login_required
def dashboardHome(request):
    customer = request.user.customer
    print(customer)
    print(customer.nutritionofcustomer)
    height = request.user.customer.nutritionofcustomer.latestHeight
    weight = request.user.customer.nutritionofcustomer.latestWeight
    bmi = request.user.customer.nutritionofcustomer.latestBMI
    gender = request.user.customer.nutritionofcustomer.gender   
    date = request.user.customer.nutritionofcustomer.day
    print(date)
    month = request.user.customer.nutritionofcustomer.month
    year = request.user.customer.nutritionofcustomer.year
    dob = str(date) + " - " + str(month) + " - " + str(year)
    print(request.user.customer.nutritionofcustomer)
    context = {
        "height": height,
        "weight": weight,
        "bmi": bmi,
        "gender": gender,
        "dob": dob
    }
    # context = {}
    return render(request,'nutrition/dashboard.html',context)

@login_required
def waterManager(request):
    if request.method == 'POST':
        try:
            glassesOfWater = request.POST.get("water")
            print(glassesOfWater)
            water = Water.objects.create(nutrition=request.user.customer.nutritionofcustomer)
            water.glasses = glassesOfWater
            water.save()
            return render(request,'nutrition/water.html',{'water':glassesOfWater})
        except:
            raise("The object is None")
    else:
        return render(request,'nutrition/water.html',{})

@login_required
def calorieManager(request):
    if request.method == 'POST':
        bmiData = {}
        height = float(request.POST.get("height"))
        heightUnit = request.POST.get("heightUnit")
        weight = float(request.POST.get("weight"))
        weightUnit = request.POST.get("weightUnit")
        bodymass = BodyMass.objects.create(nutrition=request.user.customer.nutritionofcustomer)
        bodymass.calculateBMI(height,weight,heightUnit,weightUnit)
        bodymass.save()
        request.user.customer.nutritionofcustomer.latestBMI = bodymass.bmi
        request.user.customer.nutritionofcustomer.latestHeight = bodymass.height
        request.user.customer.nutritionofcustomer.latestWeight = bodymass.weight
        print("I am here")
        gender = request.POST.get("gender")
        dob = request.POST.get("dob")
        print("Am i here")
        if gender != None:
            request.user.customer.nutritionofcustomer.gender = gender
        if dob != None:
            print(dob)
            date = int(dob[8:10])
            print(date)
            month = int(dob[5:7])
            print(month)
            year = int(dob[0:4])
            print(year)
            request.user.customer.nutritionofcustomer.day = date
            request.user.customer.nutritionofcustomer.month = month
            request.user.customer.nutritionofcustomer.year = year
        activity = request.POST.get("activity")
        request.user.customer.nutritionofcustomer.save()
        age = request.user.customer.nutritionofcustomer.calculateAge()
        calories = getExpectedEnergyRequirement(activity,age,height,weight,gender)
        bmiData["bmi"] = bodymass.bmi
        bmiData["category"] = bodymass.category
        bmiData["calories"] = calories
        return render(request,'nutrition/calorie.html',{'bmiData':bmiData})
    else:
        return render(request,'nutrition/calorie.html',{})

@login_required
def sleepManager(request):
    if request.method == 'POST':
        try:
            bmiData = {}
            sleepDuration = request.POST["sleep"]
            print(sleepDuration)
            bmiData["sleep"] = sleepDuration
            sleepObj = Sleep.objects.create(nutrition=request.user.customer.nutritionofcustomer)
            sleepObj.duration = sleepDuration
            sleepObj.save()
            return render(request,'nutrition/sleep.html',{'bmiData':bmiData})
        except:
            raise("The object is None")
    else:
        return render(request,'nutrition/sleep.html',{})

def showChartView(request,chartType):
    if chartType == "water":
        waterlist = []
        x = []
        for _ in request.user.customer.nutritionofcustomer.water_set.all():
            print(_)
            waterlist.append(_.glasses)
            x.append(_.date)
        chartLabel = "Water consumption Analysis"
        chartData = waterlist
        labels = x
    elif chartType == "sleep":
        sleeplist = []
        x = []
        for _ in request.user.customer.nutritionofcustomer.sleep_set.all():
            print(_)
            sleeplist.append(_.duration)
            x.append(_.date)
        chartLabel = "Sleep Duration Analysis"
        chartData = sleeplist
        labels = x
    elif chartType == "calorie":
        calorielist = []
        x = []
        for _ in request.user.customer.nutritionofcustomer.calorie_set.all():
            print(_)
            calorielist.append(_.calories)
            x.append(_.date)
        chartLabel = "Calorie Consumption Analysis"
        chartData = calorielist
        labels = x
    else:
        chartLabel = "Other Analysis"
        chartData = [0,10,2,34,90,78,100]
        labels = [0,1,2,3,4,5,6]
    data = {
        "labels": labels,
        "chartData": chartData,
        "chartLabel": chartLabel
    }
    return JsonResponse(data)