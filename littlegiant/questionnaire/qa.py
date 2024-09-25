import os
import django

# Add the root directory of your project to sys.path
# sys.path.append(os.path.join(os.path.dirname(__file__), 'questionnaire'))

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "questionnaire.settings")
django.setup()

from questions.models import Client
from questions.models import Question
from questions.models import Choice
from questions.models import Answer

# Fetch the questions and choices
Fragen = Question.objects.filter(category='Creative').order_by('display_order')

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
        # print(state.selected_choices[f'frage_{i}'])
        state.answers[i].selected_choice = frage.get_choice_by_symbol(
            symbol=state.selected_choices[f'frage_{i}']
            )
        # print(state.answers[i].question)
        # print(state.answers[i].selected_choice)

    # print(state.answers)


def weigh_score(state):
    print("Calculate selected items")
    print("-----------")
    # Assume answers is a list of Answer objects
    total_score = sum(answer.selected_choice.score for answer in state.answers)
    state.score = total_score
    print("The score: ", state.score)

# ------------------------------
# ! selected choices with symbol_no, not data model
# ------------------------------

selected_choices = {}
for i, frage in enumerate(Fragen):
    # print(frage.identifier, frage.text)
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

# print(answers)

# Create the questionnaire page with Taipy GUI Builder (TGB)
from taipy.gui import Gui
import taipy.gui.builder as tgb

# Use Taipy GUI Builder (TGB) to display all questions and choices
with tgb.Page() as page:
    # Title and Theme Toggle
    tgb.toggle(theme=True)
    tgb.text("### {app_title}", mode="md", class_name="text-center pb1")

    # Note: Question List
    with tgb.layout(columns="1 2 1", class_name="text-center"):
        with tgb.part():
            tgb.text(f"", mode="md")

        with tgb.part(class_name="text-left"):
            # Loop through all questions using enumerate and display them dynamically
            for i, frage in enumerate(Fragen):
                # Display the question text
                tgb.text(f"#### {i+1}.{frage.text}", mode="md")

                # Display selector for each question's choices
                # NOTE: Difference between Django data model and Pydantic 
                tgb.selector(
                    value="{selected_choices.frage_" + str(i) + "}",
                    lov=frage.get_choices(),  # Get the choices for each question
                    type=Choice,
                    adapter=choice_adapter,
                    on_change=get_selected,  # Callback for when the selection changes
                )

    # Note: submit and score
    with tgb.layout(columns="1 1 1 1", class_name="text-center"):
        with tgb.part():
            tgb.text("")

        # Submit button
        with tgb.part():
            tgb.button(
                label="Submit",
                class_name="mt2",
                on_action=weigh_score
            )

        with tgb.part():
            tgb.text(f"Score", mode="md")
            tgb.text("{score}", mode="md")

        with tgb.part():
            tgb.text("")

# ------------------------------
# Main app
# ------------------------------

if __name__ == "__main__":
    print("Starting Questionnaire app...")

    # Initialize and run the GUI
    app_title = "创新型企业问卷"
    score = 0
    gui = Gui(page=page)
    gui.run(port=5000, reload=True)
