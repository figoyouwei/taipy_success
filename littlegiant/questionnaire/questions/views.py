# questions/views.py
from django.shortcuts import render
from django.shortcuts import redirect

def home_view(request):
    return render(request, 'home.html')

def taipy_one(request):
    # Redirect to external URL (127.0.0.1:5000)
    return redirect('http://127.0.0.1:5000')

def taipy_two(request):
    # Redirect to external URL (127.0.0.1:5000)
    return redirect('http://127.0.0.1:5001')