from django.contrib import admin
from .models import Question, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice  # Show choices inline when creating/editing questions
    # extra = 3  # Number of extra blank choices to show

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'category', 'created_at', 'identifier')
    inlines = [ChoiceInline]  # Add the choices inline in the question admin interface

admin.site.register(Question, QuestionAdmin)  # Register the Question model
