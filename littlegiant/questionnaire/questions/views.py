# questions/views.py
from django.shortcuts import render

def home_view(request):
    return render(request, 'home.html')

def taipy_home(request):
    return render(request, 'home.html')