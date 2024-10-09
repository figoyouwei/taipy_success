import taipy.gui.builder as tgb
from pages.sidebar import sidebar_partial
layout_columns = "2 8"

with tgb.Page() as page:
    with tgb.layout(columns=layout_columns):
        with tgb.part("sidebar"):
            sidebar_partial()  # Render sidebar content
        
        with tgb.part():
            tgb.navbar()
            tgb.html("h1", "Service Pricing")
            tgb.html("p", "All prices are shown in United States Dollars (USD) to ensure clarity for international customers.")
            
            tgb.html("h2", "Service Packages")
            tgb.html("ul", children=[
                tgb.html("li", "Software Development: $50 USD per hour"),
                tgb.html("li", "Data Management: $55 USD per hour"),
                tgb.html("li", "Data Analysis: $55 USD per hour"),
                tgb.html("li", "LLM Applications: $60 USD per hour"),
            ])
            
            tgb.html(
                "p", 
                "Please contact us for custom pricing options or to discuss any international requirements.",
                style="color: orange;"
                )
