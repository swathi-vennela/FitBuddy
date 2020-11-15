from django.urls import path
from . import views

urlpatterns = [
    path('',views.dashboardHome,name="dashboardHome"),
    path('water/',views.waterManager,name="water"),
    path('sleep/',views.sleepManager,name="sleep"),
    path('calorie/',views.calorieManager,name="calorie"),
    path('nutritionAnalysis/',views.nutritionAnalyzer,name="analyzeNutrition"),
]