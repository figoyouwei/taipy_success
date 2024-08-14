'''
@author: Youwei Zheng
@target: on_change
@source: https://docs.taipy.io/en/develop/tutorials/visuals/1_the_on_change_callback/
@update: 2024.08.13
'''

import taipy.gui.builder as tgb
from taipy.gui import Gui

def fahrenheit_to_celsius(fahrenheit):
    fh = (fahrenheit - 32) * 5 / 9
    return round(fh, 2)

fahrenheit = 100
celsius = fahrenheit_to_celsius(fahrenheit)

def update_celsius(state):
    state.celsius = fahrenheit_to_celsius(state.fahrenheit)

# ------------------------------
# Creating page object
# ------------------------------

def create_page(changer=update_celsius):
        
    with tgb.Page() as page:
        # title line
        tgb.toggle(theme=True)
        tgb.text("# Fahrenheit to Celsius", mode="md", class_name="text-center pb1")
            
        # input fields or use number
        with tgb.layout("1 1", class_name="pb1"):
            # Fahrenheit input field
            with tgb.part(class_name="card text-center"):
                tgb.number(
                    label="Fahrenheit",
                    value="{fahrenheit}",
                    on_change=changer
                )
            
            # Celsius display field (set as inactive)
            with tgb.part(class_name="card text-center"):
                tgb.number(
                    label="Celsius",
                    value="{celsius}",
                    active=False,
                    on_change=changer
                )

        # footer
        tgb.text("Developed by CR7", mode="md", class_name="text-center pb1")               
    
    return page

# ------------------------------
# Creating page object
# ------------------------------

if __name__ == "__main__":
    page = create_page()
    Gui(page=page).run()
