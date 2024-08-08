'''
@author: Youwei Zheng
@target: Main app with just one page
@update: 2024.08.08
'''

from taipy.gui import Gui

# same code as before
from pages.home import home_md

# run GUI
Gui(page=home_md).run()