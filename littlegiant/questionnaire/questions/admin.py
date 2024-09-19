from django.contrib import admin
from .models import Question, Choice, Client

from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

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
# ChoiceInline
# ------------------------------

class ChoiceInlineFormset(BaseInlineFormSet):
    def clean(self):
        super().clean()
        symbols = []
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                symbol = form.cleaned_data.get('symbol')
                if symbol in symbols:
                    raise ValidationError("Choices for the same question must have unique symbols.")
                symbols.append(symbol)

class ChoiceInline(admin.TabularInline):
    model = Choice
    formset = ChoiceInlineFormset  # Use the custom formset to validate symbols
    extra = 0  # Number of extra blank choices to show
     
# ------------------------------
# QuestionAdmin
# ------------------------------

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'category', 'display_order', 'created_at')
    list_display_links = ('text',)  # Make the text field clickable
    list_filter = ('category',)  # Add filter by category
    ordering = ('display_order',)  # Default order by display_order
    inlines = [ChoiceInline]  # Add the choices inline in the question admin interface

admin.site.register(Question, QuestionAdmin)  # Register the Question model
