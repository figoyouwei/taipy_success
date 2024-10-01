# sidebar
import taipy.gui.builder as tgb

def sidebar_partial():
    # tgb.html("h2", "Richard Hendricks")
    # tgb.html("p", "Founder of Pied Piper")
    tgb.html(
        "link",
        "",
        href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css",
        rel="stylesheet"
    )

    tgb.html(
        "div",
        children=[
            tgb.html("img", "", src="./static/images/Profile2024.jpg", style="border-radius:50%; width:150px; height:150px; display:block; margin: 0 auto;"),  # Image with rounded corners
            tgb.html("h2", "Michael Jordan", style="text-align:center; color:white;"),  # Name
            tgb.html("div", "Basketballer", style="text-align:center; background-color:#333; padding:5px 10px; border-radius:15px; color:white;"),  # Role

            tgb.html("div", "", style="border-bottom: 1px solid #555; margin:20px 0;"),  # Separator

            tgb.html("div", children=[
                tgb.html("i", "", className="fa fa-envelope", style="color:white; margin-right:10px;"),  # Email Icon
                tgb.html("span", "jordan@qq.com", style="color:white;")
            ], style="display:flex; align-items:center; margin-bottom:15px;"),  # Email Section

            tgb.html("div", children=[
                tgb.html("i", "", className="fa fa-phone", style="color:white; margin-right:10px;"),  # Phone Icon
                tgb.html("span", "400-8888-400", style="color:white;")
            ], style="display:flex; align-items:center; margin-bottom:15px;"),  # Phone Section

            tgb.html("div", children=[
                tgb.html("i", "", className="fa fa-map-marker", style="color:white; margin-right:10px;"),  # Location Icon
                tgb.html("span", "Shanghai", style="color:white;")
            ], style="display:flex; align-items:center; margin-bottom:15px;"),  # Location Section
        ],
    )
