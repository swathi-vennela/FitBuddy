from django.shortcuts import render, redirect
from .forms import NutritionExtractionForm
from django.contrib.auth.decorators import login_required
import requests

def getIdealCalorieIntake(request):
    pass

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
            request.user.customer.nutrition.calories = calories
            print(request.user.customer.nutrition.calories)
        else:
            print(form.errors)
    else:
        form = NutritionExtractionForm()
    context["form"] = form
    return render(request,"nutrition/calorie.html",context)

def dashboardHome(request):
    return render(request,'nutrition/home.html')

def waterManager(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                bmiData = {}
                glassesOfWater = request.POST.get("water")
                print(glassesOfWater)
                request.user.customer.nutrition.waterIntake = glassesOfWater
                request.user.customer.save()
                print(request.user.customer.nutrition.waterIntake)
                bmiData["water"] = glassesOfWater
                return render(request,'nutrition/water.html',{'bmiData':bmiData})
            except:
                raise("The object is None")
        else:
            return render(request,'nutrition/water.html',{})
    else:
        return render(request,'nutrition/water.html',{})

def calorieManager(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            try:    
                bmiData = {}
                height = int(request.POST["height"])
                heightUnit = request.POST["heightUnit"]
                print(height)
                print(heightUnit)
                weight = int(request.POST["weight"])
                weightUnit = request.POST["weightUnit"]
                print(weight)
                print(weightUnit)
                bmi = calculateBMI(height,weight,heightUnit,weightUnit)
                category = findCategoryOfBMI(bmi)
                print("This is the request")
                print(request)
                print("---")
                print(request.user.customer)
                request.user.customer.nutrition.bmi = bmi
                request.user.customer.save()
                print("the bmi is ")
                print(request.user.customer.nutrition.bmi)
                bmiData["bmi"] = bmi
                bmiData["category"] = category
                return render(request,'nutrition/calorie.html',{'bmiData':bmiData})
            except:
                raise("The object is None")
        else:
            return render(request,'nutrition/calorie.html',{})
    else:
        return render(request,'nutrition/calorie.html',{})

def sleepManager(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                bmiData = {}
                sleepDuration = request.POST["sleep"]
                print(sleepDuration)
                request.user.customer.nutrition.sleepDuration = sleepDuration
                request.user.customer.save()
                print(request.user.customer.nutrition.sleepDuration)
                bmiData["sleep"] = sleepDuration
                return render(request,'nutrition/sleep.html',{'bmiData':bmiData})
            except:
                raise("The object is None")
        else:
            return render(request,'nutrition/sleep.html',{})
    else:
        return render(request,'nutrition/sleep.html',{})

# Create your views here.
def nutrition(request):
    # if request.user.is_authenticated:
    #     if request.method == 'POST':
    #         bmiData = {}
    #         if "height" in request.POST and "weight" in request.POST:
    #             
    #         if "sleep" in request.POST:
    #             
    #         if "water" in request.POST:
    #             glassesOfWater = request.POST["water"]
    #             print(glassesOfWater)
    #             request.user.customer.nutrition.waterIntake = glassesOfWater
    #             request.user.customer.save()
    #             print(request.user.customer.nutrition.waterIntake)
    #             bmiData["water"] = glassesOfWater
    #         return render(request,'nutrition/main.html',{'bmiData':bmiData})
    #     else:
    #         return render(request,'nutrition/main.html',{})
    # else:
    #     print(request.method)
    #     print("NO, I am here")
    #     return render(request,'nutrition/main.html',{})
    return render(request,"nutrition/dashboard.html")

def calculateBMI(height,weight,heightUnit,weightUnit):
    if heightUnit == 'cm':
        height = height/100.0
    elif heightUnit == 'inch':
        height = height * 0.0254
    if weightUnit == 'lb':
        weight = weight * 0.453592
    print(height)
    print(weight)
    return weight/(height*height)

def findCategoryOfBMI(bmi):
    if bmi <= 18.5:
        return "underweight"
    elif bmi <=24.9 and bmi >= 18.5:
        return "normal weight"
    elif bmi >= 25 and bmi <= 29.9:
        return "overweight"
    else:
        return "obese"