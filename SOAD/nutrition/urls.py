from django.urls import path
from .views import *

urlpatterns = [
    path('',dashboardHome,name="dashboardHome"),
    path('water/',waterManager,name="water"),
    path('sleep/',sleepManager,name="sleep"),
    path('calorie/',calorieManager,name="calorie"),
    path('nutritionAnalysis/',nutritionAnalyzer,name="analyzeNutrition"),
    # path('chart', line_chart, name='line_chart'),
    # path('chartJSON', line_chart_json, name='line_chart_json'),
]