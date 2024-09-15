import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "questionnaire.settings")
django.setup()

from questions.models import Question
from questions.models import Choice

# Fetch the questions and choices
Fragen = Question.objects.all()[2:4]  
Choices = Fragen

selected_choice = Choice()

def choice_adapter(cho: Choice):
    print(cho.symbol)
    choice_text = "{}: {}".format(cho.symbol, cho.text)
    return (cho.symbol_no, choice_text)    

def get_selected(state):
    print("Getting selected items")
    print(state.selected_choice)

# Create the questionnaire page with Taipy GUI Builder (TGB)
from taipy.gui import Gui
import taipy.gui.builder as tgb

# Use Taipy GUI Builder (TGB) to display all questions and choices
with tgb.Page() as page:
    # Title and Theme Toggle
    tgb.toggle(theme=True)
    tgb.text("### SaaS Questionnaire", mode="md", class_name="text-center pb1")

    # Loop through all questions and their corresponding choices
    with tgb.layout(columns="1 2 1", class_name="text-center"):
        with tgb.part():
            tgb.text(f"", mode="md")

        with tgb.part(class_name="text-left"): 
            # Loop through all questions using enumerate and display them dynamically
            for i, frage in enumerate(Fragen):
                # Display the question text
                tgb.text(f"#### {frage.text}", mode="md")
                
                # Display selector for each question's choices
                tgb.selector(
                    value=selected_choice,
                    lov=frage.get_choices(),  # Get the choices for each question
                    type=Choice,
                    adapter=choice_adapter,
                    on_change=get_selected  # Callback for when the selection changes
                )
            
            # Submit button
            tgb.button(
                label="Submit", 
                class_name="mt2",
                )

        with tgb.part():
            tgb.text(f"Score", mode="md")

# ------------------------------
# Main app
# ------------------------------
        
if __name__ == "__main__":
    print("Starting Questionnaire app...")

    # Initialize and run the GUI
    gui = Gui(page)
    gui.run()
