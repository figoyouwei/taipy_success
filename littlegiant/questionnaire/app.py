import os
import django

# Add the root directory of your project to sys.path
# sys.path.append(os.path.join(os.path.dirname(__file__), 'questionnaire'))

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "questionnaire.settings")
django.setup()

from questions.models import Question
from questions.models import Choice
from questions.models import Answer

# Fetch the questions and choices
Fragen = Question.objects.all()[0:3]
Choices = Fragen

def choice_adapter(cho: Choice):
    if type(cho) is Choice:
        choice_text = "{}: {}".format(cho.symbol, cho.text)
        return (cho.symbol, choice_text)
    else:
        return None

# NOTE: associate with symbols, not the enumerated
def select_user(state, var_name: str, value) -> None:
    print("The user selected: {}".format(state.selected_user.name))
    
def get_selected(state):
    print("Getting selected items")
    print("-----------")
    for i, frage in enumerate(Fragen):
        state.answers[i].question = frage
        print(state.selected_choices[f'frage_{i}'])
        state.answers[i].selected_choice = frage.get_choice_by_symbol(
            symbol=state.selected_choices[f'frage_{i}']
            )
        # print(state.answers[i].question)
        # print(state.answers[i].selected_choice)

    print(state.answers)


def weigh_score(state):
    print("Getting selected items")
    print("-----------")
    for i, frage in enumerate(Fragen):
        print(frage.text)
        print(f"Selected: {selected_choices[f'frage_{i}']}")

    state.score = 8
    print("The score: ", state.score)

# ------------------------------
# ! selected choices with symbol_no, not data model
# ------------------------------

selected_choices = {}
for i, frage in enumerate(Fragen):
    print(frage.identifier, frage.text)
    selected_choices[f"frage_{i}"] = "A"

# ------------------------------
# answer instances
# ------------------------------

answers = []
for i, frage in enumerate(Fragen):
    ans = Answer()
    ans.question = frage
    ans.selected_choice = frage.get_choice_by_symbol(symbol="A")
    answers.append(ans)

print(answers)

score = 0

# Create the questionnaire page with Taipy GUI Builder (TGB)
from taipy.gui import Gui
import taipy.gui.builder as tgb

# Use Taipy GUI Builder (TGB) to display all questions and choices
with tgb.Page() as page:
    # Title and Theme Toggle
    tgb.toggle(theme=True)
    tgb.text("### Taipy Questionnaire", mode="md", class_name="text-center pb1")

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
                # NOTE: Difference between Django data model and Pydantic 
                tgb.selector(
                    value="{selected_choices.frage_" + str(i) + "}",
                    lov=frage.get_choices(),  # Get the choices for each question
                    type=Choice,
                    adapter=choice_adapter,
                    on_change=get_selected,  # Callback for when the selection changes
                )

            # Submit button
            tgb.button(
                label="Submit",
                class_name="mt2",
                on_action=weigh_score
            )

        with tgb.part():
            tgb.text(f"Score", mode="md")
            tgb.text("{score}", mode="md")

# ------------------------------
# Main app
# ------------------------------

if __name__ == "__main__":
    print("Starting Questionnaire app independently...")

    # Initialize and run the GUI
    gui = Gui(page=page)
    gui.run(port=5000, reload=True)
