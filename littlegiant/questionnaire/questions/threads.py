# questions/threads.py

import os
from django.apps import AppConfig
import threading
from taipy.gui import Gui
import taipy.gui.builder as tgb

# Define Taipy GUI: One (App One)
with tgb.Page() as page_one:
    tgb.text("### Welcome to Taipy App One", mode="md")
    tgb.toggle(theme=True)
    tgb.text("This is Taipy App One running alongside Django.", mode="md")

# Define Taipy GUI: Two (App Two)
with tgb.Page() as page_two:
    tgb.text("### Welcome to Taipy App Two", mode="md")
    tgb.toggle(theme=True)
    tgb.text("This is Taipy App Two running alongside Django.", mode="md")


class AppsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'questions'

    def ready(self):
        """This method runs when Django starts the application."""

        # Prevent Taipy from running in the auto-reloader process
        if os.environ.get('RUN_MAIN') != 'true':
            return
        
        # Initialize the first Taipy GUI (App One)
        gui_one = Gui(page_one)

        # Run the first Taipy app in a separate thread on port 5000
        taipy_thread_one = threading.Thread(
            target=gui_one.run, 
            kwargs={'port': 5001}, 
            daemon=True
        )
        taipy_thread_one.start()

        # Initialize the second Taipy GUI (App Two)
        gui_two = Gui(page_two)

        # Run the second Taipy app in a separate thread on port 5001
        taipy_thread_two = threading.Thread(
            target=gui_two.run, 
            kwargs={'port': 5002}, 
            daemon=True
        )
        taipy_thread_two.start()
