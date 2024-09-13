from flask import Flask, render_template
from taipy.gui import Gui
import taipy.gui.builder as tgb

# Step 1: Create a Flask app
app = Flask(__name__)

# Step 2: Define your Taipy GUI
with tgb.Page() as page:
    tgb.text("### Welcome to the Taipy App", mode="md")
    tgb.toggle(theme=True)
    tgb.text("This is a simple integration of Flask and Taipy.", mode="md")

# Step 3: Initialize the Taipy GUI
gui = Gui(page)

# Step 4: Create a Flask route for the homepage
@app.route('/')
def index():
    return render_template('index.html')  # A simple home page in Flask

# Step 5: Run the Flask app
if __name__ == '__main__':
    # Run Flask in one terminal
    app.run(debug=True, port=8000)

    # In another terminal, run Taipy on a different port, e.g., port 5001
    gui.run(port=5000)  # Run Taipy on port 5001
