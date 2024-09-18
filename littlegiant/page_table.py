# ------------------------------
# table page
# ------------------------------

import polars as pl
df_fruits = pl.DataFrame(
    {
        "fruits": ["apple", "banana", "apple", "banana", "banana"],
        "prices": [1.0, 2.0, 3.0, 4.0, 5.0],
    }
).to_pandas()

# print(df_fruits)
# print(type(df_fruits))

import taipy.gui.builder as tgb

with tgb.Page() as page:
    tgb.text("Fruit Table")
    tgb.table("{df_fruits}")

