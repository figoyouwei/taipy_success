# questionnaire/urls.py
from django.contrib import admin
from django.urls import path
from questions import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view),  # Normal Django homepage route
    path('taipy_one/', views.taipy_one, name='taipy_one'),  # Route with name
    path('taipy_two/', views.taipy_two, name='taipy_two'),  # Route with name
]