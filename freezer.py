import threading
from time import sleep
from taipy import Gui

# Background task to simulate long-running process
def background_task():
    print("Background task started.")
    sleep(10)
    print("Background task completed.")

# Start the background task on a separate thread
def start_background_task():
    threading.Thread(target=background_task).start()

# Taipy GUI definition
page = """
# Taipy App

<button on_click="start_background_task">Start Background Task</button>
<p>App will not freeze when the task is running in the background.</p>
"""

# Run the GUI with the background task button
gui = Gui(page)
gui.run()