from django.contrib import admin
from .models import Question, Choice, Client

# ------------------------------
# AnswerAdmin
# ------------------------------

# ------------------------------
# ClientAdmin
# ------------------------------

class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'company_name')  # Fields to display in the admin list view

admin.site.register(Client, ClientAdmin)

# ------------------------------
# ChoiceInline and QuestionAdmin
# ------------------------------

class ChoiceInline(admin.TabularInline):
    model = Choice  # Show choices inline when creating/editing questions
    extra = 0  # Number of extra blank choices to show

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'category', 'created_at', 'identifier')
    inlines = [ChoiceInline]  # Add the choices inline in the question admin interface

admin.site.register(Question, QuestionAdmin)  # Register the Question model
