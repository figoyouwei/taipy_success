"""
@author: Youwei Zheng
@target: better understand selector
@update: 2024.09.05
"""

import taipy.gui.builder as tgb
from taipy.gui import Gui

from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    birth_year: int

users = [
    User(id=1, name="Figo", birth_year=1987),
    User(id=2, name="John", birth_year=1979),
    User(id=3, name="Lisa", birth_year=1968),
    User(id=4, name="Mary", birth_year=1974),
    ]

selected_user = users[2]


def selector_adapter(item):
    print("Entering selector_adapter...")
    # print("Guten Morgen, {}, {}".format(item.id, item.name))    
    return (item.id, item.name + "...")


def select_user(state, var_name: str, value) -> None:
    print("The user selected: {}".format(state.selected_user.name))


with tgb.Page() as page:
    with tgb.layout("1"):
        tgb.selector(
            value="{selected_user}",
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