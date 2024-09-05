"""
@author: Youwei Zheng
@target: better understand selector
@update: 2024.09.05
"""

import taipy.gui.builder as tgb
from taipy.gui import Gui

class User:
    def __init__(self, id, name, birth_year):
        self.id, self.name, self.birth_year = (id, name, birth_year)

users = [
    User(4, "Figo", 1987),
    User(3, "John", 1979),
    User(2, "Lisa", 1968),
    User(8, "Mary", 1974)
    ]

selected_user = users[2]


def selector_adapter(item):
    print("Entering selector_adapter...")
    print("Guten Morgen, {}, {}".format(item.id, item.name))
    
    return (item.id, item.name + "...")


def select_user(state, var_name: str, value) -> None:
    print("The user selected: {}".format(state.selected_user.name))


with tgb.Page() as page:
    with tgb.layout("1"):
        tgb.selector(
            "{selected_user}",
            lov="{users}",
            # NOTE: on_change = on_click
            on_change=select_user,
            # NOTE: type = data model
            type=User,
            adapter=selector_adapter,
        )

if __name__ == "__main__":
    gui = Gui(page)

    gui.run(
        dark_mode=True, 
        title="Taipy Selector"
        )