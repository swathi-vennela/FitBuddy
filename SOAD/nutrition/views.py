from django.shortcuts import render, redirect
from .forms import NutritionExtractionForm
from django.contrib.auth.decorators import login_required
import requests
from decimal import *
import json
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView

def getExpectedEnergyRequirement(activity,age,height,weight,gender):
    if activity == "sedentary":
        physicalActivityLevel = Decimal(1.00)
    elif activity == "low active":
        physicalActivityLevel = Decimal(1.40)
    elif activity == "active":
        physicalActivityLevel = Decimal(1.60)
    else:
        physicalActivityLevel = Decimal(1.90)
    if gender == "female":
        if age < 19:
            result = Decimal(135.30) - (Decimal(30.80) * age) + physicalActivityLevel * ((Decimal(10.0) * weight) + (Decimal(934) * height)) + 25
        else:
            result = 354 - (Decimal(6.91) * age) + physicalActivityLevel * ((Decimal(9.36) * weight) + (726 * height))
    else:
        if age < 19:
            result = Decimal(88.5) - (Decimal(61.9) * age) + physicalActivityLevel * ((Decimal(26.7) * weight) + (903 * height)) + 25
        else:
            result = 662 - (Decimal(9.53) * age) + physicalActivityLevel * ((Decimal(15.91) * weight) + (Decimal(539.6) * height))
    return round(result,2)

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
            request.user.customer.nutrition.calories = calories
            print(request.user.customer.nutrition.calories)
        else:
            print(form.errors)
    else:
        form = NutritionExtractionForm()
    context["form"] = form
    return render(request,"nutrition/nutritionAnalysis.html",context)

@login_required
def dashboardHome(request):
    height = request.user.customer.nutrition.height
    weight = request.user.customer.nutrition.weight
    bmi = request.user.customer.nutrition.bmi
    gender = request.user.customer.nutrition.gender
    age = request.user.customer.nutrition.age
    print(request.user.customer.nutrition)
    context = {
        "height": height,
        "weight": weight,
        "bmi": bmi,
        "gender": gender,
        "age": age
    }
    return render(request,'nutrition/dashboard.html',context)

@login_required
def waterManager(request):
    if request.method == 'POST':
        try:
            glassesOfWater = request.POST.get("water")
            print(glassesOfWater)
            request.user.customer.nutrition.waterIntake = glassesOfWater
            request.user.customer.save()
            print(request.user.customer.nutrition.waterIntake)
            waterlist = []
            for _ in request.user.customer.nutrition_set.all():
                waterlist.append(_.waterIntake)
            x = len(waterlist)
            integers = [i for i in range(x)]
            print(json.dumps(waterlist))
            print(json.dumps(integers))
            return render(request,'nutrition/water.html',{'water':json.dumps(waterlist),'labels': json.dumps(integers)})
        except:
            raise("The object is None")
    else:
        return render(request,'nutrition/water.html',{})

@login_required
def calorieManager(request):
    if request.method == 'POST':
        bmiData = {}
        height = request.POST.get("height")
        height = Decimal(height)
        heightUnit = request.POST.get("heightUnit")
        weight = request.POST.get("weight")
        weight = Decimal(weight)
        weightUnit = request.POST.get("weightUnit")
        height = heightToMeters(height,heightUnit)
        weight = weightToKgs(weight,weightUnit)
        request.user.customer.nutrition.height = height
        request.user.customer.nutrition.weight = weight
        bmi = calculateBMI(height,weight,heightUnit,weightUnit)
        print("height is ")
        print(height)
        print("weight is ")
        print(weight)
        print("bmi is ")
        print(bmi)
        bmi = round(bmi,2)
        print(bmi)
        category = findCategoryOfBMI(bmi)
        print("category is ")
        print(category)
        request.user.customer.nutrition.bmi = bmi
        print("here?")
        request.user.customer.nutrition.save()
        print("I am here")
        gender = request.POST.get("gender")
        print("Am i here")
        if gender != None:
            request.user.customer.nutrition.gender = gender
        if request.POST.get("age") != None:
            age = int(request.POST.get("age"))
            request.user.customer.nutrition.age = age
        activity = request.POST.get("activity")
        bmiData["bmi"] = bmi
        bmiData["category"] = category
        request.user.customer.nutrition.save()
        calories = getExpectedEnergyRequirement(activity,age,height,weight,gender)
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
            request.user.customer.nutrition.sleepDuration = sleepDuration
            request.user.customer.nutrition.save()
            print(request.user.customer.nutrition.sleepDuration)
            bmiData["sleep"] = sleepDuration
            return render(request,'nutrition/sleep.html',{'bmiData':bmiData})
        except:
            raise("The object is None")
    else:
        return render(request,'nutrition/sleep.html',{})

def calculateBMI(height,weight,heightUnit,weightUnit):
    result = weight/(height*height)
    print(result)
    result = Decimal(result)
    print(result)
    return result

def findCategoryOfBMI(bmi):
    if bmi <= 18.5:
        return "underweight"
    elif bmi <=24.9 and bmi >= 18.5:
        return "normal weight"
    elif bmi >= 25 and bmi <= 29.9:
        return "overweight"
    else:
        return "obese"

def heightToMeters(height,heightUnit):
    if heightUnit == 'cm':
        height = height/Decimal(100.0)
    elif heightUnit == 'inch':
        height = height * Decimal(0.02)
    print(height)
    return Decimal(height)

def weightToKgs(weight,weightUnit):
    if weightUnit == 'lb':
        weight = weight * Decimal(0.45)
    return Decimal(weight)

# class LineChartJSONView(BaseLineChartView):
#     def get_labels(self):
#         """Return 7 labels for the x-axis."""
#         return ["January", "February", "March", "April", "May", "June", "July"]

#     def get_providers(self):
#         """Return names of datasets."""
#         return ["Central", "Eastside", "Westside"]

#     def get_data(self):
#         """Return 3 datasets to plot."""

#         return [[75, 44, 92, 11, 44, 95, 35],
#                 [41, 92, 18, 3, 73, 87, 92],
#                 [87, 21, 94, 3, 90, 13, 65]]


# line_chart = TemplateView.as_view(template_name='line_chart.html')
# line_chart_json = LineChartJSONView.as_view()