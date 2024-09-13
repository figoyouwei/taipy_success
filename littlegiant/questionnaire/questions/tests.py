from django.test import TestCase

# Create your tests here.
from questions.pages import page_one

from taipy.gui import Gui

Gui(page_one).run()