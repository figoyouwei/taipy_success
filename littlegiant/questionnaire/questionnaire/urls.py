# questionnaire/urls.py
from django.contrib import admin
from django.urls import path
from questions import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view),  # Normal Django homepage route
    path('whatever/', views.taipy_home),  # Another route for example
]
